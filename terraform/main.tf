# main.tf
provider "azurerm" {
  subscription_id = "b5925b7a-60a6-4194-8cad-165403bbc592"
  features {}
}

resource "azurerm_resource_group" "state_storage_account" {
name = "terraformdeploy-unique-1234"
location = "Brazil South"
}

resource "azurerm_virtual_network" "vnet" {
  name                = "vnet-prod"
  address_space       = ["10.0.0.0/16"]
  location            = azurerm_resource_group.state_storage_account.location
  resource_group_name = azurerm_resource_group.state_storage_account.name
}

resource "azurerm_subnet" "subnet_app" {
  name                 = "subnet-appservice"
  resource_group_name  = azurerm_resource_group.state_storage_account.name
  virtual_network_name = azurerm_virtual_network.vnet.name
  address_prefixes     = ["10.0.1.0/24"]

  delegation {
    name = "delegation-appservice"
    service_delegation {
      name = "Microsoft.Web/serverFarms"
      actions = [
        "Microsoft.Network/virtualNetworks/subnets/action"
      ]
    }
  }
}


resource "azurerm_subnet" "subnet_db" {
  name                 = "subnet-database"
  resource_group_name  = azurerm_resource_group.state_storage_account.name
  virtual_network_name = azurerm_virtual_network.vnet.name
  address_prefixes     = ["10.0.2.0/24"]

   delegation {
    name = "delegation-postgres"
    service_delegation {
      name = "Microsoft.DBforPostgreSQL/flexibleServers"
      actions = [
        "Microsoft.Network/virtualNetworks/subnets/action"
      ]
    }
  }
}

resource "azurerm_service_plan" "plan" {
  name                = "asp-exemplo-linux"
  resource_group_name = azurerm_resource_group.state_storage_account.name
  location            = azurerm_resource_group.state_storage_account.location
  os_type             = "Linux"
  sku_name            = "B1"
}

resource "azurerm_linux_web_app" "app" {
  name                = "app-exemplo-dotnet"
  resource_group_name = azurerm_resource_group.state_storage_account.name
  location            = azurerm_service_plan.plan.location
  service_plan_id     = azurerm_service_plan.plan.id

  site_config {
    application_stack {
      dotnet_version = "9.0"  # Versão do .NET
    }
  }

  app_settings = {
    "WEBSITE_RUN_FROM_PACKAGE" = "1"
    "Firebase__ProjectId" = "projeto-terraform-d8344"
  }


  zip_deploy_file = "./Confeite.zip"  # Caminho relativo ao arquivo ZIP
}

resource "azurerm_postgresql_flexible_server" "postgres" {
  name                   = "meu-postgres-server"
  resource_group_name    = azurerm_resource_group.state_storage_account.name
  location               = azurerm_resource_group.state_storage_account.location
  administrator_login    = "pgadmin"
  administrator_password = "SenhaSuperSecreta123!"
  version                = "15"
  storage_mb             = 32768
  sku_name               = "B_Standard_B1ms"
  public_network_access_enabled = false
  delegated_subnet_id    = azurerm_subnet.subnet_db.id
  private_dns_zone_id    = azurerm_private_dns_zone.postgres_dns.id
}

resource "azurerm_private_dns_zone" "postgres_dns" {
  name                = "privatelink.postgres.database.azure.com"
  resource_group_name = azurerm_resource_group.state_storage_account.name
}

resource "azurerm_private_dns_zone_virtual_network_link" "dns_link" {
  name                  = "postgres-dns-link"
  resource_group_name   = azurerm_resource_group.state_storage_account.name
  private_dns_zone_name = azurerm_private_dns_zone.postgres_dns.name
  virtual_network_id    = azurerm_virtual_network.vnet.id
}

resource "azurerm_app_service_virtual_network_swift_connection" "vnet_integration" {
  app_service_id = azurerm_linux_web_app.app.id
  subnet_id      = azurerm_subnet.subnet_app.id
}

resource "azurerm_app_service_custom_hostname_binding" "custom_domain" {
  hostname            = "robertoribeironeto.shop"
  resource_group_name = azurerm_resource_group.state_storage_account.name
  app_service_name    = azurerm_linux_web_app.app.name
}
