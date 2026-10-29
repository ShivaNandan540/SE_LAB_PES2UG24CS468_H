def coupon_discount(code, cart_total, is_new_user, day):
    if cart_total <= 0:
        raise ValueError("empty cart")
    if code == "WELCOME10":
        if is_new_user:
            return cart_total * 0.10
        return 0
    if code == "WEEKEND20":
        if day in ("sat", "sun"):
            if cart_total >= 500:
                return cart_total * 0.20
            return 50
        return 0
    if code == "FLAT100":
        if cart_total > 300:
            return 100
        return 0
    return 0


def best_discount(codes, cart_total, is_new_user, day):
    best = 0
    for code in codes:
        value = coupon_discount(code, cart_total, is_new_user, day)
        if value > best:
            best = value
    cap = cart_total * 0.4
    if best > cap:
        return cap
    return best


def is_expired(today, start, days_valid):
    if days_valid <= 0:
        return True
    return today - start > days_valid
