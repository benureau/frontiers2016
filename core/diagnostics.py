def contact_data(data):
    contacts = []
    for t, metadata in enumerate(data.data['metadata']):
        try:
            contacts.append((t, metadata['raw_sensors.salient_contacts']))
        except KeyError:
            contacts.append((t, None))

    return contacts

def contact_stats(cfg, contacts, verbose=True):
    """Extract max force events from dovecot exploration files"""
    collisions, ok_col, total = 0, 0, 0

    for t, c in contacts:
        if c is not None and c['max'] is not None:
            collisions += 1
            if verbose:
                print('{}: {} N'.format(t, c['max'].force_norm))
            if c['max'].force_norm <= cfg.exploration.env.sprims.max_force:
                ok_col += 1

        total += 1

    return collisions, ok_col, total
