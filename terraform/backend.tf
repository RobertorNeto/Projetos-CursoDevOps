terraform{
backend "azurerm"{
 resource_group_name = "myResourceGroupName"
 storage_account_name = "cursolacunadevopsstate10"
 container_name = "remote-state-tfstate"
 key = "terraform.tfstate"
}
}
