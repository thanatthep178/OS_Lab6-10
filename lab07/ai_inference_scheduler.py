from collections import deque


class AIRequest:
    def __init__(self, user_id, tokens_required):
        self.user_id = user_id
        self.tokens_required = tokens_required
        self.tokens_generated = 0
        self.first_token_time = None
        self.finish_time = None


def generate_token(req, current_time):
    # Each token costs one simulated time unit.
    current_time += 1
    req.tokens_generated += 1

    if req.first_token_time is None:
        req.first_token_time = current_time

    print(
        f"[Time {current_time:02d}] {req.user_id}: "
        f"token {req.tokens_generated}/{req.tokens_required}"
    )

    if req.tokens_generated == req.tokens_required:
        req.finish_time = current_time
        print(f"  -> {req.user_id} FINISHED")

    return current_time


def show_summary(requests):
    print("\nUser         | TTFT | Completion time")

    for req in requests:
        print(
            f"{req.user_id:12} | "
            f"{req.first_token_time:4d} | "
            f"{req.finish_time:15d}"
        )


def simulate_fcfs(requests):
    print("\n--- AI Inference: FCFS ---")
    current_time = 0

    for req in requests:
        while req.tokens_generated < req.tokens_required:
            current_time = generate_token(req, current_time)

    show_summary(requests)


def simulate_round_robin(requests):
    print("\n--- AI Inference: Round Robin (1 token per turn) ---")
    current_time = 0
    ready_queue = deque(requests)

    while ready_queue:
        req = ready_queue.popleft()
        current_time = generate_token(req, current_time)

        if req.tokens_generated < req.tokens_required:
            ready_queue.append(req)

    show_summary(requests)


def new_requests():
    return [
        AIRequest("User_A_Essay", 10),
        AIRequest("User_B_Math", 2),
    ]


def main():
    print("All requests arrive at time 0.")
    print("Each token takes 1 simulated time unit.")
    print("No real AI model or GPU is used.")

    simulate_fcfs(new_requests())
    simulate_round_robin(new_requests())


if __name__ == "__main__":
    main()