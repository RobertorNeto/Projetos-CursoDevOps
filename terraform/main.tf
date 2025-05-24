# main.tf
provider "azurerm" {
  features {}
}

resource "azurerm_service_plan" "plan" {
  name                = "asp-exemplo-linux"
  resource_group_name = azurerm_resource_group.state-storage-account.name
  location            = azurerm_resource_group.state-storage-account.location
  os_type             = "Linux"
  sku_name            = "B1"
}

resource "azurerm_linux_web_app" "app" {
  name                = "app-exemplo-dotnet"
  resource_group_name = azurerm_resource_group.state-storage-account.name
  location            = azurerm_service_plan.plan.location
  service_plan_id     = azurerm_service_plan.plan.id

  site_config {
    application_stack {
      dotnet_version = "8.0"  # Versão do .NET
    }
  }

  app_settings = {
    "WEBSITE_RUN_FROM_PACKAGE" = "1"
    "Firebase__ProjectId" = "projeto-terraform-d8344"
  }


  zip_deploy_file = "./Confeite.zip"  # Caminho relativo ao arquivo ZIP
}
