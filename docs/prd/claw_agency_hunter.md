# PRD - Claw Agency Hunter

## Objetivo
Criar um agente autônomo baseado no framework OpenClaw para prospecção de leads no Upwork, pesquisa profunda e geração de propostas personalizadas.

## Stack Técnica
- **Framework**: OpenClaw (Node.js 22+)
- **LLM Primário**: Groq (llama-3.3-70b-versatile)
- **LLM Fallback**: Gemini 2.0 Flash
- **Banco de Dados**: PostgreSQL (Railway)
- **Fila**: Redis (Railway)
- **Habilidades (Skills)**: AutoResearch, Superpowers, Hunter (Apify)

## Funcionalidades
1. **Hunter**: Scraper do Upwork via Apify para encontrar leads baseados em palavras-chave.
2. **AutoResearch**: Pesquisa profunda sobre o cliente e o projeto para enriquecer a proposta.
3. **Superpowers**: Acesso ao sistema de arquivos e shell para automação local.
4. **Notificações**: Integração com Telegram para alertas e controle do agente.

## Configuração de Deploy
- **Plataforma**: Railway
- **Porta**: 18789
- **Modo Gateway**: Local (Containerizado)
