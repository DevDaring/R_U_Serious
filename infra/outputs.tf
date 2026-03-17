output "droplet_ip" {
  description = "Public IP of the FunLearn Droplet — use this to access the app"
  value       = digitalocean_droplet.funlearn_app.ipv4_address
}

output "ritty_agent_id" {
  description = "ID of the Ritty Gradient AI Agent"
  value       = digitalocean_gradientai_agent.ritty.id
}

output "ncert_kb_id" {
  description = "ID of the NCERT Knowledge Base"
  value       = digitalocean_gradientai_knowledge_base.ncert_kb.id
}

output "volume_id" {
  description = "ID of the persistent CSV data volume"
  value       = digitalocean_volume.funlearn_data.id
}
