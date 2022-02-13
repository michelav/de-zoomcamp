output "control_machine_address" {
  description = "Control Machine IP"
  value       = google_compute_instance.control_machine.network_interface.0.access_config.0.nat_ip
}

output "ssh_config" {
  description = "SSH Config File"
  sensitive   = true
  value = templatefile("ssh_config.tftpl", { ip = google_compute_instance.control_machine.network_interface.0.access_config.0.nat_ip,
  user = var.ssh_username })
}