resource "digitalocean_gradientai_knowledge_base" "ncert_kb" {
  name        = "ncert-curriculum-kb"
  description = "NCERT and CBSE curriculum content for Feynman Engine and Story Learning"
  region      = "tor1"

  web_crawler_data_source = {
    base_url        = "https://ncert.nic.in/textbook.php"
    crawling_option = "SCOPED"
    embed_media     = false
  }
}

resource "digitalocean_gradientai_agent" "ritty" {
  name        = "Ritty-Feynman-Agent"
  model       = "meta-llama/Meta-Llama-3.3-70B-Instruct"
  description = "Ritty is a curious 8-year-old AI child who helps students learn through the Feynman Technique"

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

  knowledge_base_ids = [digitalocean_gradientai_knowledge_base.ncert_kb.uuid]

  depends_on = [digitalocean_gradientai_knowledge_base.ncert_kb]
}
