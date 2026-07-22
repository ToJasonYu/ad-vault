import argparse
import csv
import os
import random
from dataclasses import asdict, dataclass
from datetime import datetime, timedelta

CATEGORIES = ["sports", "tech", "travel", "finance", "gaming"]
DEVICE_TYPES = ["mobile", "desktop", "tablet"]
AGE_BRACKETS = ["18-24", "25-34", "35-44", "45-54", "55+"]

NAME_PREFIXES = ["Blue", "Summit", "Northline", "Horizon", "Cedar", "Bright", "Union", "Silver", "Vertex", "Harbor"]
NAME_SUFFIXES = ["Labs", "Group", "Co", "Works", "Partners", "Media", "Studio", "Collective", "Systems", "Ventures"]

# click-probability model: base rate + boost when the user's interest matches
# the ad's category + a small device effect + noise, clamped to a sane range
BASE_CLICK_RATE = 0.02
SEGMENT_MATCH_BOOST = 0.06
DEVICE_BOOST = {"mobile": 0.01, "desktop": 0.0, "tablet": -0.005}
NOISE_RANGE = 0.01
MIN_CLICK_PROB = 0.001
MAX_CLICK_PROB = 0.95

ON_BRAND_CAMPAIGN_RATE = 0.85
DAYS_BACK = 30


@dataclass
class Advertiser:
    advertiser_id: str
    name: str
    industry: str


@dataclass
class Campaign:
    campaign_id: str
    advertiser_id: str
    category: str
    budget: float
    bid_amount: float


@dataclass
class User:
    user_id: str
    age_bracket: str
    interest_segment: str
    device_type: str


@dataclass
class Event:
    event_id: str
    user_id: str
    campaign_id: str
    timestamp: str
    clicked: int


def generate_advertisers(n):
    advertisers = []

    for i in range(1, n + 1):
        industry = random.choice(CATEGORIES)
        name = f"{random.choice(NAME_PREFIXES)} {random.choice(NAME_SUFFIXES)}"
        advertiser_id = f"adv_{i:04d}"
        advertisers.append(Advertiser(advertiser_id, name, industry))

    return advertisers


def generate_campaigns(advertisers, campaigns_per_advertiser):
    campaigns = []
    campaign_counter = 1

    for advertiser in advertisers:
        for _ in range(campaigns_per_advertiser):
            on_brand = random.random() < ON_BRAND_CAMPAIGN_RATE
            category = advertiser.industry if on_brand else random.choice(CATEGORIES)
            budget = round(random.uniform(500, 20000), 2)
            bid_amount = round(random.uniform(0.20, 5.00), 2)
            campaign_id = f"camp_{campaign_counter:04d}"

            campaigns.append(Campaign(campaign_id, advertiser.advertiser_id, category, budget, bid_amount))
            campaign_counter += 1

    return campaigns


def generate_users(n):
    users = []

    for i in range(1, n + 1):
        user_id = f"user_{i:05d}"
        age_bracket = random.choice(AGE_BRACKETS)
        interest_segment = random.choice(CATEGORIES)
        device_type = random.choice(DEVICE_TYPES)

        users.append(User(user_id, age_bracket, interest_segment, device_type))

    return users


def click_probability(user, campaign):
    prob = BASE_CLICK_RATE

    if user.interest_segment == campaign.category:
        prob += SEGMENT_MATCH_BOOST

    prob += DEVICE_BOOST[user.device_type]
    prob += random.uniform(-NOISE_RANGE, NOISE_RANGE)

    return min(max(prob, MIN_CLICK_PROB), MAX_CLICK_PROB)


def generate_events(users, campaigns, n_events):
    events = []
    now = datetime.now()

    for i in range(1, n_events + 1):
        user = random.choice(users)
        campaign = random.choice(campaigns)
        prob = click_probability(user, campaign)
        clicked = 1 if random.random() < prob else 0
        offset_seconds = random.randint(0, DAYS_BACK * 24 * 3600)
        timestamp = (now - timedelta(seconds=offset_seconds)).isoformat()
        event_id = f"evt_{i:06d}"

        events.append(Event(event_id, user.user_id, campaign.campaign_id, timestamp, clicked))

    return events


def write_csv(path, rows):
    if not rows:
        return

    fieldnames = list(asdict(rows[0]).keys())

    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(asdict(row))


def main():
    parser = argparse.ArgumentParser(description="Generate synthetic ad-vault data")
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--n-advertisers", type=int, default=40)
    parser.add_argument("--campaigns-per-advertiser", type=int, default=3)
    parser.add_argument("--n-users", type=int, default=2000)
    parser.add_argument("--n-events", type=int, default=50000)
    parser.add_argument("--output-dir", default="output")
    args = parser.parse_args()

    random.seed(args.seed)

    advertisers = generate_advertisers(args.n_advertisers)
    campaigns = generate_campaigns(advertisers, args.campaigns_per_advertiser)
    users = generate_users(args.n_users)
    events = generate_events(users, campaigns, args.n_events)

    os.makedirs(args.output_dir, exist_ok=True)
    write_csv(os.path.join(args.output_dir, "advertisers.csv"), advertisers)
    write_csv(os.path.join(args.output_dir, "campaigns.csv"), campaigns)
    write_csv(os.path.join(args.output_dir, "users.csv"), users)
    write_csv(os.path.join(args.output_dir, "events.csv"), events)

    click_count = sum(event.clicked for event in events)
    overall_ctr = click_count / len(events)

    print(f"generated {len(advertisers)} advertisers, {len(campaigns)} campaigns, {len(users)} users, {len(events)} events")
    print(f"overall CTR: {overall_ctr:.4f}")


if __name__ == "__main__":
    main()
