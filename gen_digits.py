import random
from itertools import product, permutations
import json
import shutil
import datetime
import time


def gen_nums(m, c_low, c_high):
    n = []
    odd_count = 0
    even_count = 0
    while len(set(n)) < m:
        i = random.randint(c_low, c_high)
        if len(n) == 0 or (
            i not in n
            and (
                ((i % 2 == 0) and (even_count <= 3)) or ((i % 2 == 1) and (odd_count <= 3))
            )
            # (min(abs(x - i) for x in n) > 1)
        ):
            n.append(i)
            if (i % 2) == 0:
                even_count += 1
            else:
                odd_count += 1
    sep_count = 0
    sorted_n = sorted(n)
    for i in range(len(n) - 1):
        for j in range(len(n) - 1):
            if abs(sorted_n[i] - sorted_n[j + 1]) == 1:
                sep_count += 1
    if sep_count >= 3:
        return gen_nums(m, c_low, c_high)  
    return n


def calc(m, c_low, c_high, t_low, t_high, t_prob_thresh):
    # Get a set of composite numbers
    n = gen_nums(m, c_low, c_high)

    ops = ["+", "-", "*", "/"]
    l = set()
    how = dict()
    op_how = dict()
    c_counts = dict()
    _comp_done = dict()
    for perm in permutations(n, m):
        for op in product(ops, repeat=m - 1):
            s = 0
            st = ""
            opies = ""
            c = list(perm)
            for i, o in enumerate(op):
                form = f"({c[i]} {o} {c[i + 1]})"
                if i == 0:
                    opies += f"{c[i]} {o} {c[i + 1]} "
                else:
                    opies += f"{o} {c[i + 1]} "
                try:
                    s = _comp_done[form]
                except KeyError:
                    if "+" in form:
                        s = c[i] + c[i + 1]
                    elif "-" in form:
                        s = c[i] - c[i + 1]
                    elif "*" in form:
                        s = c[i] * c[i + 1]
                    elif "/" in form:
                        s = c[i] / c[i + 1]
                    _comp_done[form] = s
                # s = eval(form)
                c[i + 1] = s
                st += form + " --> "
                if int(s) == s and s > 0 and s <= 10_000:
                    ans = int(s)
                    if sorted(opies.strip().split()) not in op_how.get(ans, []):
                        final_form = st + f" --> {ans}"
                        final_form = final_form.replace("-->  -->", "-->")
                        l.add(ans)
                        how[ans] = how.get(ans, []) + [
                            final_form.replace("-->  -->", "-->")
                        ]
                        op_how[ans] = op_how.get(ans, []) + [
                            sorted(opies.strip().split())
                        ]
                        c_counts[ans] = c_counts.get(ans, 0) + 1
                else:
                    break
    # Just take the targets that are less than 600
    c_counts = {k: v for k, v in c_counts.items() if t_low <= k <= t_high}
    # Randomly select a number that's in the bottom portion of the frequency
    freq = dict()
    i = 1
    for k, v in sorted(c_counts.items(), key=lambda item: item[1]):
        freq[k] = v
        if i / len(c_counts) > t_prob_thresh:
            break
        i += 1
    target, n_ways = random.choice(list(freq.items()))
    how = {k: v for k, v in how.items() if k == target}
    return sorted(n), how, c_counts, target, n_ways


def write_digits(filepath):
    d = {
        "puzzleDate": (
            datetime.datetime.utcnow() + datetime.timedelta(days=1)
        ).strftime("%Y-%m-%d")
    }
    # Range from 2, 30
    # Round 1:
    # Composite: [2, 15]
    # Target: [55, 160]
    # Select in bottom half
    m = 6
    c_low, c_high = 2, 15
    t_low, t_high = 85, 160
    t_prob_thresh = 0.5
    n, how, c_counts, target, n_ways = calc(
        m, c_low, c_high, t_low, t_high, t_prob_thresh
    )
    d["r1"] = {
        "n": n,
        "how": how,
        # "c_counts": c_counts,
        "target": target,
        "n_ways": n_ways,
        "round": 1,
    }
    print("Round 1 Done")

    # Round 2:
    # Composite: [3, 20]
    # Target: [140, 255]
    # Select in bottom half
    c_low, c_high = 3, 20
    t_low, t_high = 140, 255
    t_prob_thresh = 0.5
    n, how, c_counts, target, n_ways = calc(
        m, c_low, c_high, t_low, t_high, t_prob_thresh
    )
    d["r2"] = {
        "n": n,
        "how": how,
        # "c_counts": c_counts,
        "target": target,
        "n_ways": n_ways,
        "round": 2,
    }
    print("Round 2 Done")

    # Round 3:
    # Composite: [3, 20]
    # Target: [220, 360]
    # Select in bottom half
    c_low, c_high = 3, 20
    t_low, t_high = 220, 360
    t_prob_thresh = 0.5
    n, how, c_counts, target, n_ways = calc(
        m, c_low, c_high, t_low, t_high, t_prob_thresh
    )
    d["r3"] = {
        "n": n,
        "how": how,
        # "c_counts": c_counts,
        "target": target,
        "n_ways": n_ways,
        "round": 3,
    }
    print("Round 3 Done")

    # Round 4:
    # Composite: [4, 25]
    # Target: [325, 465]
    # Select in bottom third
    c_low, c_high = 4, 25
    t_low, t_high = 325, 465
    t_prob_thresh = 0.33
    n, how, c_counts, target, n_ways = calc(
        m, c_low, c_high, t_low, t_high, t_prob_thresh
    )
    d["r4"] = {
        "n": n,
        "how": how,
        # "c_counts": c_counts,
        "target": target,
        "n_ways": n_ways,
        "round": 4,
    }
    print("Round 4 Done")

    # Round 5:
    # Composite: [4, 25]
    # Target: [430, 600]
    # Select in bottom quarter
    c_low, c_high = 4, 25
    t_low, t_high = 430, 600
    t_prob_thresh = 0.25
    n, how, c_counts, target, n_ways = calc(
        m, c_low, c_high, t_low, t_high, t_prob_thresh
    )
    d["r5"] = {
        "n": n,
        "how": how,
        # "c_counts": c_counts,
        "target": target,
        "n_ways": n_ways,
        "round": 5,
    }
    print("Round 5 Done")

    with open(filepath, "w") as f:
        json.dump(d, f)


if __name__ == "__main__":
    # For testing retry
    # r = random.random()
    # if r < 0.333:
    #     print("Sleeping")
    #     time.sleep(200)
    # elif r >= 0.333 and r <= 0.666:
    #     print("Error")
    #     raise ValueError("Error")
    # else:
    #     print("Success")

    
    # today --> yesterday
    shutil.copyfile("data/data_today.json", "data/data_yesterday.json")
    # tomorrow --> today
    shutil.copyfile("data/data_tomorrow.json", "data/data_today.json")
    write_digits("data/data_tomorrow.json")
