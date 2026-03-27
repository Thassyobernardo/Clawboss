#!/usr/bin/env python3
"""Persistência de leads do Hunter em PostgreSQL (via DATABASE_URL). Use com a ferramenta exec."""
import argparse
import json
import sys

from db import get_connection


def save_from_payload(payload: dict) -> int:
    required = ("titulo", "dor_cliente", "como_escalar", "faturar_2k_mes")
    missing = [k for k in required if not str(payload.get(k, "")).strip()]
    if missing:
        raise ValueError(f"Campos obrigatórios ausentes ou vazios: {', '.join(missing)}")

    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """
        INSERT INTO hunter_leads (titulo, dor_cliente, como_escalar, faturar_2k_mes, fonte)
        VALUES (%s, %s, %s, %s, %s)
        RETURNING id;
        """,
        (
            payload["titulo"].strip(),
            payload["dor_cliente"].strip(),
            payload["como_escalar"].strip(),
            payload["faturar_2k_mes"].strip(),
            (payload.get("fonte") or "").strip() or None,
        ),
    )
    row = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()
    return int(row["id"])


def main() -> None:
    p = argparse.ArgumentParser(description="Grava lead do Hunter no banco (SQL/PostgreSQL).")
    sub = p.add_subparsers(dest="cmd", required=True)

    save_p = sub.add_parser("save", help="Insere um lead a partir de JSON.")
    save_p.add_argument(
        "payload_json",
        help='JSON com titulo, dor_cliente, como_escalar, faturar_2k_mes (opcional: fonte). Ex.: \'{"titulo":"..."}\'',
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
        try:
            new_id = save_from_payload(data)
        except Exception as e:
            print(str(e), file=sys.stderr)
            sys.exit(1)
        print(json.dumps({"ok": True, "id": new_id}))


if __name__ == "__main__":
    main()
