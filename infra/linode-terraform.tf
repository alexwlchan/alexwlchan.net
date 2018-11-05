variable "linode_api_token" {}

provider "linode" {
  token = "${var.linode_api_token}"
}

resource "linode_instance" "helene" {
  type  = "g6-standard-1"
  region = "eu-west"

  config {
    label  = "My Ubuntu 16.04 LTS Profile"
    kernel = "linode/latest-64bit"
  }

  disk {
    label = "Ubuntu 16.04 LTS Disk"
    size  = 50944
  }

  disk {
    label = "256MB Swap Image"
    size  = 256
  }
}
