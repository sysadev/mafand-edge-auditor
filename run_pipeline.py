import sys
import time
from src.ingest import stream_mafand_data
from src.gates import audit_sentence_pair
from src.storage import AuditDatabase

BATCH_SIZE = 1000  # Hold 1,000 rows in RAM (~200KB), then flush to disk


def main():
    print("\n[+] Booting Hausa NLP Data Fidelity Auditor...")
    start_time = time.time()

    db = AuditDatabase()
    db.reset_laboratory()
    data_stream = stream_mafand_data()

    batch_buffer = []
    total_processed = 0

    print("[+] Conveyor belt running. Auditing pairs...")

    for row in data_stream:
        src = row["source_text"]
        tgt = row["target_text"]
        raw_id = row["raw_row_id"]

        is_valid, gate_failed, reason = audit_sentence_pair(src, tgt)

        batch_buffer.append({
            "raw_row_id": raw_id,
            "source_text": src,
            "target_text": tgt,
            "is_valid": is_valid,
            "gate_failed": gate_failed,
            "error_reason": reason
        })

        total_processed += 1

        # When the bucket gets full, dump it into SQLite
        if len(batch_buffer) >= BATCH_SIZE:
            db.insert_batch(batch_buffer)
            batch_buffer.clear()

            # '\r' overwrites the exact same line in place
            sys.stdout.write(f"\r    ... audited {total_processed:,} pairs")
            sys.stdout.flush()

    # Catch the remaining leftovers sitting in the bucket (e.g. the final 412 rows)
    if batch_buffer:
        db.insert_batch(batch_buffer)
        batch_buffer.clear()

    elapsed = time.time() - start_time
    print(f"\r[✓] Audit Complete: {total_processed:,} pairs processed in {elapsed:.2f}s.")

    # --- THE ACADEMIC MONEY SHOT ---
    print("\n" + "=" * 52)
    print("             EMPIRICAL AUDIT TAXONOMY")
    print("=" * 52)

    raw_stats = db.get_summary_stats()

    # Sort so 'PASSED' sits at the top, then order errors by highest volume
    stats_sorted = sorted(raw_stats, key=lambda x: (x[0] != "PASSED", -x[1]))

    for gate, count in stats_sorted:
        pct = (count / total_processed) * 100 if total_processed > 0 else 0
        print(f" {gate:<26} | {count:>7,} rows  ({pct:>5.1f}%)")

    print("=" * 52 + "\n")


if __name__ == "__main__":
    main()
