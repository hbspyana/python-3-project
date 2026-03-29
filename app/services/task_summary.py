def summarize_attendance(records):
    total = len(records)
    present = len([r for r in records if r.status == 'present'])
    return {'total': total, 'present': present, 'percentage': (present / total * 100) if total > 0 else 0}