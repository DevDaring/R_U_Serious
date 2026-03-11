resource "digitalocean_volume" "funlearn_data" {
  region                   = var.region
  name                     = "funlearn-data"
  size                     = 5
  initial_filesystem_type  = "ext4"
  description              = "Persistent CSV storage for FunLearn app"
}

resource "digitalocean_volume_attachment" "funlearn_data_attach" {
  droplet_id = digitalocean_droplet.funlearn_app.id
  volume_id  = digitalocean_volume.funlearn_data.id
}
