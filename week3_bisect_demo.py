from bisect import insort


account_ids = [101, 105, 110]

print("Before:", account_ids)

insort(account_ids, 103)

print("After:", account_ids)