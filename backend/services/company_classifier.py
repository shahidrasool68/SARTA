"""Company tier classification and initial difficulty mapping for SARTA.

Companies are classified into three tiers based on interview difficulty:
  - HARD  → MAANG, top quant/fintech, and elite tech companies
  - EASY  → Large service/consulting companies with standard interviews
  - MEDIUM → Everything else (default)

The tier determines the *starting* MCQ difficulty for adaptive assessment.
After the first question, the adaptive controller (CAT) takes over.
"""

# ── Company Tier Lists ──────────────────────────────────────────────────

HARD_COMPANIES = {
    # MAANG / Big Tech
    "google", "meta", "amazon", "apple", "netflix", "microsoft",
    # Top Tech
    "uber", "airbnb", "linkedin", "stripe", "palantir technologies",
    "tesla", "bytedance", "tiktok", "openai", "databricks", "snowflake",
    "coinbase", "doordash", "snap", "pinterest", "spotify", "twitter", "x",
    "nvidia", "adobe", "salesforce", "dropbox", "lyft", "robinhood",
    "roblox", "instacart", "reddit", "duolingo", "cloudflare",
    # Quant / Trading / Finance (elite)
    "citadel", "two sigma", "jane street", "de shaw", "hudson river trading",
    "jump trading", "optiver", "tower research capital", "sig",
    "squarepoint capital", "drw", "akuna capital",
    # Finance (top tier)
    "goldman sachs", "morgan stanley", "j.p. morgan", "bloomberg",
    "blackrock",
    # Other elite
    "atlassian", "databricks", "scale ai", "cruise", "waymo", "nuro",
    "aurora", "applied intuition", "anduril",
}

EASY_COMPANIES = {
    # Service / Consulting companies
    "tcs", "infosys", "wipro", "hcl", "cognizant", "tech mahindra",
    "capgemini", "accenture", "mindtree", "lti", "genpact",
    "dxc technology", "coforge", "mphasis", "hexaware",
    "larsen & toubro", "persistent systems", "nagarro",
    "publicis sapient", "thoughtworks", "ey", "pwc", "deloitte",
    "virtusa", "epam systems", "luxoft", "softwire",
    # Indian IT / Mid-tier
    "amdocs", "cedcoss", "maq software", "wissen technology",
    "altimetrik", "consultadd", "mountblue", "zopsmart",
    "hashedin", "hilabs", "josh technology", "fpt",
}


def classify_company_tier(company_name: str) -> str:
    """Classify a company into 'HARD', 'MEDIUM', or 'EASY' tier.
    
    Returns:
        str: one of 'HARD', 'MEDIUM', 'EASY'
    """
    if not company_name:
        return "MEDIUM"
    
    name_lower = company_name.strip().lower()
    
    if name_lower in HARD_COMPANIES:
        return "HARD"
    if name_lower in EASY_COMPANIES:
        return "EASY"
    return "MEDIUM"


def initial_difficulty_for_tier(tier: str) -> str:
    """Map company tier to the starting MCQ difficulty.
    
    - EASY  companies → start with Easy questions (build confidence, then adapt up)
    - MEDIUM companies → start with Medium questions (standard baseline)
    - HARD  companies → start with Hard questions (challenge first, then adapt down)
    """
    return {
        "EASY": "Easy",
        "MEDIUM": "Medium",
        "HARD": "Hard",
    }.get(tier, "Medium")


def get_company_assessment_config(company_name: str) -> dict:
    """Return full assessment configuration for a given company.
    
    Example:
        >>> get_company_assessment_config("Google")
        {'company': 'Google', 'tier': 'HARD', 'initial_difficulty': 'Hard'}
    """
    tier = classify_company_tier(company_name)
    return {
        "company": company_name,
        "tier": tier,
        "initial_difficulty": initial_difficulty_for_tier(tier),
    }

