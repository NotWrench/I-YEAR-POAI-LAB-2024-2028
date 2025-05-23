import ast


class BlocksWorld:
    def __init__(self, num_blocks):
        if not isinstance(num_blocks, int) or num_blocks < 0:
            raise ValueError(
                "Number of blocks must be a non-negative integer.")
        self.state = [[block] for block in range(num_blocks)]
        self.num_blocks = num_blocks

    def display_state(self):
        for stack in self.state:
            print(f"Block(s) on stack: {stack}")
        if not self.state and self.num_blocks > 0:
            pass
        elif not self.state and self.num_blocks == 0:
            print("No blocks in the world.")

    def move(self, block, destination):
        source_stack = self.find_block(block)
        destination_stack = self.find_block(destination)

        if source_stack is None or destination_stack is None:
            print(f"Invalid block {block} or destination {destination}.")
            return

        if block not in source_stack:
            print(
                f"Error: Block {block} not found in its expected source stack. State might be inconsistent.")
            return

        try:
            source_stack.remove(block)
        except ValueError:
            print(f"Error: Block {block} could not be removed from its stack.")
            return

        destination_stack.append(block)
        self.state = [s for s in self.state if s]
        self.display_state()

    def find_block(self, block_id):
        for stack in self.state:
            if block_id in stack:
                return stack
        return None

    def goal_state(self, goal):
        if not isinstance(goal, list):
            print("Error: Goal configuration must be a list of stacks.")
            return

        all_blocks_in_goal = []
        expected_blocks = set(range(self.num_blocks))

        for stack_idx, stack_content in enumerate(goal):
            if not isinstance(stack_content, list):
                print(
                    f"Error: Stack {stack_idx} in goal configuration is not a list.")
                return
            for block_in_stack in stack_content:
                if not isinstance(block_in_stack, int) or block_in_stack < 0 or block_in_stack >= self.num_blocks:
                    print(
                        f"Error: Invalid block ID {block_in_stack} in goal configuration. Blocks are 0 to {self.num_blocks-1}.")
                    return
                if block_in_stack in all_blocks_in_goal:
                    print(
                        f"Error: Block {block_in_stack} is duplicated in goal configuration.")
                    return
                all_blocks_in_goal.append(block_in_stack)

        if set(all_blocks_in_goal) != expected_blocks:
            print(
                f"Error: Goal configuration must contain all blocks from 0 to {self.num_blocks-1} exactly once and without extras.")
            return

        self.state = goal
        print("Goal state set.")
        self.display_state()


def main():
    try:
        num_blocks_str = input("Enter the number of blocks: ")
        num_blocks = int(num_blocks_str)
        if num_blocks < 0:
            print("Number of blocks must be a non-negative integer.")
            return
        blocks_world = BlocksWorld(num_blocks)
    except ValueError:
        print("Invalid input for number of blocks. Please enter an integer.")
        return

    print("\nInitial state:")
    blocks_world.display_state()

    goal_input_str = input(
        f"\nEnter a goal state configuration (e.g., [[0,1],[2]] for {num_blocks} blocks, or press Enter to skip): ").strip()
    if goal_input_str:
        try:
            goal_config = ast.literal_eval(goal_input_str)
            blocks_world.goal_state(goal_config)
        except (ValueError, SyntaxError):
            print(
                "Invalid format for goal state. Must be a Python-style list of lists (e.g., [[0,1],[2]]).")
        except Exception as e:
            print(f"Error processing goal state: {e}")

    print("\nPerforming Moves:")
    while True:
        action_input = input(
            "\nEnter move as 'B D' (move block B onto stack of block D), or 'done' to quit: ").strip()

        if not action_input:
            continue

        if action_input.lower() == 'done':
            print("Exiting.")
            break

        parts = action_input.split()
        if len(parts) == 2:
            try:
                block_to_move = int(parts[0])
                destination_block_id = int(parts[1])

                if not (0 <= block_to_move < blocks_world.num_blocks):
                    print(
                        f"Error: Block to move {block_to_move} is invalid. Must be between 0 and {blocks_world.num_blocks-1}.")
                    continue
                if not (0 <= destination_block_id < blocks_world.num_blocks):
                    print(
                        f"Error: Destination block {destination_block_id} is invalid. Must be between 0 and {blocks_world.num_blocks-1}.")
                    continue

                blocks_world.move(block_to_move, destination_block_id)
            except ValueError:
                print("Invalid block IDs. Both must be integers.")
            except Exception as e:
                print(f"An unexpected error occurred: {e}")
        else:
            print("Invalid input format. Enter as 'B D' (e.g., '0 2') or 'done'.")

    print("\nFinal state:")
    blocks_world.display_state()


if __name__ == "__main__":
    main()
