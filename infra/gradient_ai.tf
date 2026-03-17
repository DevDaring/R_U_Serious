# Look up the default project
data "digitalocean_project" "default" {
  name = "first-project"
}

# Look up available Gradient AI models (for embedding model UUID)
data "digitalocean_gradientai_models" "all" {}

# Look up available Gradient AI regions
data "digitalocean_gradientai_regions" "all" {}

# Find the embedding model UUID (use first foundational model)
locals {
  # GTE Large EN v1.5 — a proper embedding model for knowledge base vectorization
  embedding_model_uuid = "22653204-79ed-11ef-bf8f-4e013e2ddde4"
  # Llama 3.3 Instruct (70B) for the agent
  llama_model_uuid = "d754f2d7-d1f0-11ef-bf8f-4e013e2ddde4"
  # Use tor1 for Gradient AI (supported region)
  gradient_region = "tor1"
}

# Knowledge Base with NCERT curriculum
resource "digitalocean_gradientai_knowledge_base" "ncert_kb" {
  name                 = "ncert-curriculum-kb"
  region               = local.gradient_region
  project_id           = data.digitalocean_project.default.id
  embedding_model_uuid = local.embedding_model_uuid

  datasources {
    web_crawler_data_source {
      base_url        = "https://ncert.nic.in/textbook.php"
      crawling_option = "SCOPED"
      embed_media     = false
    }
  }
}

# Ritty AI Agent
resource "digitalocean_gradientai_agent" "ritty" {
  name        = "Ritty-Feynman-Agent"
  description = "Ritty is a curious 8-year-old AI child who helps students learn through the Feynman Technique"
  region      = local.gradient_region
  project_id  = data.digitalocean_project.default.id
  model_uuid  = local.llama_model_uuid

  instruction = <<-PROMPT
    You are Ritty, a curious and enthusiastic 8-year-old child who LOVES learning new things.
    Your job is NOT to teach — your job is to be taught by the student.
    Ask one simple "Why?" or "How?" question at a time.
    If the student's explanation is confusing, say "I don't get it, can you say it simpler?"
    If the explanation is clear, say "Oh! So it's like..." and make a childlike analogy.
    Never give the answer. Always ask questions.
    Keep responses under 3 sentences.
    Respond in whatever language the student is using.
    You are safe, kind, and never use adult language.
  PROMPT

  knowledge_base_uuid = [digitalocean_gradientai_knowledge_base.ncert_kb.id]

  depends_on = [digitalocean_gradientai_knowledge_base.ncert_kb]
}
