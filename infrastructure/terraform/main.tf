provider "azurerm" {
  features {}
}

provider "aws" {
  region = var.aws_region
}

resource "azurerm_resource_group" "residency" {
  name     = "rg-${var.project_name}-residency-${var.environment}"
  location = var.location
}

# --- Residency Control Plane (AKS) ---

resource "azurerm_kubernetes_cluster" "residency_k8s" {
  name                = "aks-sovereign-iq-${var.environment}"
  location            = azurerm_resource_group.residency.location
  resource_group_name = azurerm_resource_group.residency.name
  dns_prefix          = "residency-k8s"

  default_node_pool {
    name       = "default"
    node_count = 3
    vm_size    = "Standard_D2s_v3"
  }

  identity {
    type = "SystemAssigned"
  }
}

# --- Residency Metadata Store (Postgres) ---

resource "azurerm_postgresql_flexible_server" "metadata" {
  name                   = "psql-sovereign-metadata-${var.environment}"
  resource_group_name    = azurerm_resource_group.residency.name
  location               = azurerm_resource_group.residency.location
  version                = "13"
  administrator_login    = "sovadmin"
  administrator_password = var.db_password
  storage_mb             = 32768
  sku_name               = "GP_Standard_D2ds_v4"
}

# --- Regional Sovereign Landing Zones (EU Example) ---

resource "azurerm_virtual_network" "eu_boundary" {
  name                = "vnet-eu-data-boundary"
  location            = "westeurope"
  resource_group_name = azurerm_resource_group.residency.name
  address_space       = ["10.10.0.0/16"]
  
  tags = {
    SovereigntyZone = "EU-EFTA"
    DataResidency   = "Compliant"
  }
}

# --- Multi-Cloud Sovereignty Archive (AWS S3) ---

resource "aws_s3_bucket" "sovereign_archive" {
  bucket = "sovereign-data-archive-${var.environment}"
  
  tags = {
    Jurisdiction = "US-Legal"
  }
}
