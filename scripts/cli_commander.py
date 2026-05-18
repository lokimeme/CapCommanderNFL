import argparse
import sys
from backend.app.core.database import SessionLocal
from backend.app.models.player import Player
from backend.app.models.contract import Contract
from backend.app.services.cba_rules import calculate_detailed_cut_impact
from backend.app.services.trade_engine import calculate_player_trade_impact

def run_forensic_cli():
    parser = argparse.ArgumentParser(description="🏈 CapCommander CLI Forensic Suite")
    subparsers = parser.add_subparsers(dest="command", help="Sub-commands")

    # Cut Analysis
    cut_parser = subparsers.add_parser("cut", help="Analyze player cut impact")
    cut_parser.add_argument("--player", required=True, help="Player name or GSIS ID")
    cut_parser.add_argument("--post-june", action="store_true", help="Calculate as Post-June 1st")

    # Trade Analysis
    trade_parser = subparsers.add_parser("trade", help="Analyze player trade impact")
    trade_parser.add_argument("--player", required=True, help="Player name or GSIS ID")
    trade_parser.add_argument("--retention", type=float, default=0.0, help="Salary retention percentage (0.0 - 1.0)")

    # Roster List
    list_parser = subparsers.add_parser("list", help="List team roster")
    list_parser.add_argument("--team", required=True, help="Team abbreviation (e.g., KC)")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    db = SessionLocal()
    try:
        if args.command == "list":
            players = db.query(Player).filter(Player.team_abbr == args.team).all()
            print(f"--- Roster for {args.team} ---")
            for p in players:
                print(f"[{p.position}] {p.name} ({p.gsis_id})")

        elif args.command == "cut":
            player = db.query(Player).filter(Player.name.ilike(f"%{args.player}%")).first()
            if not player:
                print(f"Player {args.player} not found.")
                return
            
            contract = db.query(Contract).filter(Contract.player_id == player.gsis_id).first()
            if not contract:
                print("No contract data found.")
                return

            impact = calculate_detailed_cut_impact(contract, 2024)
            move = "post_june_1" if args.post_june else "pre_june_1"
            print(f"--- Cut Impact for {player.name} ({move.upper()}) ---")
            print(f"Immediate Savings: ${impact[move]['savings']:.2f}M")
            print(f"Dead Cap Incurred: ${impact[move].get('dead_cap', impact[move].get('dead_cap_current')):.2f}M")
            if args.post_june:
                print(f"Future Dead Cap (2025): ${impact[move]['dead_cap_future']:.2f}M")

        elif args.command == "trade":
            player = db.query(Player).filter(Player.name.ilike(f"%{args.player}%")).first()
            if not player:
                print(f"Player {args.player} not found.")
                return
            
            contract = db.query(Contract).filter(Contract.player_id == player.gsis_id).first()
            impact = calculate_player_trade_impact(contract, 2024, args.retention)
            
            print(f"--- Trade Impact for {player.name} ---")
            print(f"Trading Team Savings: ${impact['trading_team']['immediate_savings']:.2f}M")
            print(f"Trading Team Dead Cap: ${impact['trading_team']['dead_cap_added']:.2f}M")
            print(f"Receiving Team Cap Hit: ${impact['receiving_team']['new_cap_hit']:.2f}M")

    finally:
        db.close()

if __name__ == "__main__":
    run_forensic_cli()
