from beartype import beartype

from sotopia.messages import Message, ScriptEnvironmentResponse


@beartype
class RuleBasedResponse:
    def __init__(self) -> None:
        pass

    def __call__(
        self,
        turn_number: int,
        inbox: list[tuple[str, Message]],
        initial_response: ScriptEnvironmentResponse,
    ) -> ScriptEnvironmentResponse:
        return self.rule_based_response(turn_number, inbox, initial_response)

    @beartype
    def rule_based_response(
        self,
        turn_number: int,
        inbox: list[tuple[str, Message]],
        initial_response: ScriptEnvironmentResponse,
    ) -> ScriptEnvironmentResponse:
        # Rule 1: If the conversation is too long, terminate the conversation
        if turn_number > 20:
            initial_response.conversation_too_long = True
            initial_response.terminated = True
        # Rule 2: If one of the players leaves, terminate the conversation
        if len(inbox) > 1 and "leave" in inbox[-2][1].to_natural_language():
            initial_response.p1_leaving = True
            initial_response.terminated = True
        if len(inbox) and "leave" in inbox[-1][1].to_natural_language():
            initial_response.p2_leaving = True
            initial_response.terminated = True
        # Rule 3: If the conversation is stale for too long, terminate the conversation
        stale_count = 0
        for message in inbox[::-1]:
            if message[0] == "Environment":
                continue
            if "did nothing" in message[1].to_natural_language():
                stale_count += 1
            else:
                break
            if stale_count > 5:
                initial_response.stale_too_long = True
                initial_response.terminated = True
        return initial_response
