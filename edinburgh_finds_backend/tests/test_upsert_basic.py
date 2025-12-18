# tests/test_upsert_basic.py

from sqlmodel import Session
from sqlalchemy import select, delete
from database.engine import engine
from database.db_models import Listing, Venue
from schemas.venue_extraction_schema import VenueSchema
from services.upsert_entity import upsert_from_schema


def run_test():
    entity_name = "Example Sports Club"
    entity_type = "venue"

    print("\n=== TEST RUN #1 (initial insert) ===")

    dto_1 = VenueSchema(
        street_address="123 Example Street",
        city="Edinburgh",
        postcode="EH1 2AB",
        phone="+44 131 000 0000",
        website_url="https://exampleclub.co.uk",
        tennis_total_courts=5,
        field_confidence={
            "street_address": 0.92,
            "city": 0.95,
            "postcode": 0.91,
            "phone": 0.88,
            "website_url": 0.90,
            "tennis_total_courts": 0.75,
        },
        source_info={"sources": ["https://exampleclub.co.uk"]}
    )

    listing, venue, report = upsert_from_schema(
        data=dto_1,
        entity_name=entity_name,
        entity_type=entity_type,
    )

    print("listing changes:", report["listing_changes"])
    print("entity changes:", report["entity_changes"])

    print("\n=== DB State After PASS #1 ===")
    print(listing)
    print(venue)

    print("\n=== TEST RUN #2 (update attempt) ===")

    # Same values except website_url changes AND phone confidence increases
    dto_2 = VenueSchema(
        website_url="https://exampleclub.com",  # different → triggers confidence gating
        phone="+44 131 000 0000",               # same value but higher confidence
        field_confidence={
            "website_url": 0.70,  # BELOW threshold → should NOT overwrite
            "phone": 0.97,        # ABOVE old_conf → should overwrite confidence
        },
        source_info={"sources": ["https://google.com/maps/place/exampleclub"]}
    )

    listing, venue, report = upsert_from_schema(
        data=dto_2,
        entity_name=entity_name,
        entity_type=entity_type,
    )

    print("listing changes:", report["listing_changes"])
    print("entity changes:", report["entity_changes"])

    print("\n=== DB State After PASS #2 ===")
    print(listing)
    print(venue)


if __name__ == "__main__":
    # Optional: start clean
    with Session(engine) as session:
        # Delete the venue tied to the specific listing
        session.exec(
            delete(Venue).where(
                Venue.listing_id.in_(
                    select(Listing.listing_id).where(Listing.entity_name == "Example Sports Club")
                )
            )
        )

        # Delete the listing itself
        session.exec(
            delete(Listing).where(Listing.entity_name == "Example Sports Club")
        )

        session.commit()

    run_test()
