packer {
  required_plugins {
    googlecompute = {
      version = ">= 0.0.1"
      source  = "github.com/hashicorp/googlecompute"
    }
  }
}

variable "project_id" {
  type = string
}

variable "source_image_family" {
  type    = string
  default = "ubuntu-2004-lts"
}

variable "zone" {
  type    = string
  default = "southamerica-west1-a"
}

variable "ssh_username" {
  type = string
}

variable "ssh_private_key_file" {
  type = string
}

variable "machine_type" {
  type    = string
  default = "e2-standard-2"
}

variable "image_name" {
  type    = string
  default = "de-packer-{{timestamp}}"
}

source "googlecompute" "control_machine" {
  project_id           = var.project_id
  source_image_family  = var.source_image_family
  zone                 = var.zone
  image_description    = "Created with Packer"
  ssh_username         = var.ssh_username
  ssh_private_key_file = var.ssh_private_key_file
  machine_type         = var.machine_type
  image_name           = var.image_name
  tags                 = ["packer"]
}

build {
  name    = "gcp"
  sources = ["sources.googlecompute.control_machine"]

  provisioner "shell" {
    inline = [
      "wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O ~/miniconda.sh",
      "sh miniconda.sh -b -p $HOME/miniconda && $HOME/miniconda/bin/conda init",
      "echo 'debconf debconf/frontend select Noninteractive' | sudo debconf-set-selections && sudo apt-get update && sudo apt-get install -y docker.io docker-compose git",
      "sudo usermod -aG docker ${var.ssh_username}"
    ]
  }
}