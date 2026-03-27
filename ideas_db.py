#!/usr/bin/env python3
"""INSERT na tabela `projects` (aba Ideias do Dashboard). Preferir este comando via exec em vez de arquivos .md."""
import argparse
import json
import sys

from db import insert_idea_from_research


def main() -> None:
    p = argparse.ArgumentParser(
        description="INSERT SQL-equivalente em projects (titulo, descricao, potencial_lucro, escalabilidade)."
    )
    sub = p.add_subparsers(dest="cmd", required=True)
    save_p = sub.add_parser("save", help="Insere ideia pendente a partir de JSON.")
    save_p.add_argument(
        "payload_json",
        help='JSON: {"titulo":"...","descricao":"...","potencial_lucro":"...","escalabilidade":"..."}',
    )
    save_p.add_argument(
        "--price-aud",
        type=float,
        default=35.0,
        help="Preço sugerido AUD (legado do dashboard).",
    )

    args = p.parse_args()
    if args.cmd == "save":
        try:
            data = json.loads(args.payload_json)
        except json.JSONDecodeError as e:
            print(f"JSON inválido: {e}", file=sys.stderr)
            sys.exit(2)
        if not isinstance(data, dict):
            print("O payload JSON deve ser um objeto.", file=sys.stderr)
            sys.exit(2)
        req = ("titulo", "descricao", "potencial_lucro", "escalabilidade")
        missing = [k for k in req if not str(data.get(k, "")).strip()]
        if missing:
            print(f"Campos obrigatórios: {', '.join(missing)}", file=sys.stderr)
            sys.exit(2)
        try:
            new_id = insert_idea_from_research(
                data["titulo"],
                data["descricao"],
                data["potencial_lucro"],
                data["escalabilidade"],
                price_aud=args.price_aud,
            )
        except Exception as e:
            print(str(e), file=sys.stderr)
            sys.exit(1)
        print(json.dumps({"ok": True, "id": new_id, "table": "projects"}))


if __name__ == "__main__":
    main()
