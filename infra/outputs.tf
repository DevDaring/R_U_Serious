output "droplet_ip" {
  description = "Public IP of the FunLearn Droplet — use this to access the app"
  value       = digitalocean_droplet.funlearn_app.ipv4_address
}

output "ritty_agent_uuid" {
  description = "UUID of the Ritty Gradient AI Agent — add this to backend .env as RITTY_AGENT_UUID"
  value       = digitalocean_gradientai_agent.ritty.uuid
}

output "ncert_kb_uuid" {
  description = "UUID of the NCERT Knowledge Base"
  value       = digitalocean_gradientai_knowledge_base.ncert_kb.uuid
}

output "volume_id" {
  description = "ID of the persistent CSV data volume"
  value       = digitalocean_volume.funlearn_data.id
}
