# HealthAId

<div align="center">
    <img src="./assets/logo.png" />
</div>

<div align="center">
    <span>Imagine going to a pharmacist and seeing someone like this - how does that sound?</span>
</div>

<div style="padding: 5%;">


A next-gen model leveraging the power of the company's existing knowledge base and foundational models.

Why not leverage the power of reasoning, prompt chains, and other such innovations, to give your users the ability to chat with it? Think of interacting with a pharmacist on the fly who knows about the current status of stocks in your website.

[*Original submission (During Bajaj HackRx 4.0)*](https://github.com/hackrx40/PS1-undefined_neq_null/tree/anuran)

[**Pitch Deck**](https://pitch.com/public/a8a8e20a-f446-4d56-a1ae-9ced887e551a)

Made by Team **undefined != null** ([Abhishek](https://github.com/Abhii-Agarwal09), [Anuran](https://github.com/anuran-roy), [Dhaval](https://github.com/dhavalkolhe/dhavalkolhe) and [Samridhhi]()) with ❤️.

## Features

- **Hackable**: Want to add some other model? Sure, go ahead! Want to add new data sources? Be our guest! Want to add a new feature? Likewise, go ahead!

- **Plug-and-play**: You can use it right out of the box by just specifying the required environment variables - nothing extra needed.

- **Adaptable** - The prompts are super easy to change. You can add new prompts, and the model will adapt to it - since it's a foundational model.

## Architecture

```mermaid
    graph LR;
    subgraph anuran["LLM Operations (LLMOps) Section (in Python)"]
        data
        db
        prompt
        prompt1
        prompt2
        prompt3
        scraper
        scraper1
        scraper2
        caller
        caller1
        caller2
        caller3
    end

    subgraph abhishek["User Auth + Chat History Section (in ExpressJS)"]
        auth
        logger
        mongodb
    end

    subgraph dhaval["Frontend Section (in NextJS)"]
        frontend
    end

    user[User] --> |1| frontend[Frontend]
    frontend --> |2| auth["Authentication + Chat storage APIs (in NodeJS)"]
    auth --> |3| logger["Chat History Logger (in NodeJS)"]
    logger --> |3.1| mongodb["Storing history in MongoDB"]
    mongodb --> |3.2| logger
    logger --> |4| data["LLM Gateway"]
    
    data --> |4.1| db["Cache/Database (Redis Cache or ElasticSearch DB)"]
    db --> |"4.1.1 (If data not found)"| scraper(("Scraper engines (in Python)"))
    scraper --> |"4.1.1.1 (Request)"| scraper1[MayoClinic Scraper]
    scraper1 --> |"4.1.1.2 (Response)"| scraper
    scraper --> |"4.1.1.1 (Request)"| scraper2[Drugs.com Scraper]
    scraper2 --> |"4.1.1.2 (Response)"| scraper
    scraper --> |4.1.2| db
    db --> |4.2| data
    data --> |4.3| prompt(("Prompt Engine/Aggregator"))
    prompt --> |"4.3.1 (Request)"| prompt1["Prompt 1"]
    prompt1 --> |"4.3.2 (Response)"| prompt
    prompt --> |"4.3.1 (Request)"| prompt2["Prompt 2"]
    prompt2 --> |"4.3.2 (Response)"| prompt
    prompt --> |"4.3.1 (Request)"| prompt3["Prompt 3"]
    prompt3 --> |"4.3.2 (Response)"| prompt
    prompt --> |4.4| data
    data --> |4.5| caller(("Model callers"))
    caller --> |"4.5.1 (Request)"| caller1[OpenAI GPT-3]
    caller1 --> |"4.5.2 (Response)"| caller
    caller --> |"4.5.1 (Request)"| caller2[OpenAI GPT-4]
    caller2 --> |"4.5.2 (Response)"| caller
    caller --> |"4.5.1 (Request)"| caller3[Anthropic Claude]
    caller3 --> |"4.5.2 (Response)"| caller
    caller --> |"4.6 (Answer)"| data
    data --> |5| logger
    logger --> |6| frontend
    frontend --> |7| user
```