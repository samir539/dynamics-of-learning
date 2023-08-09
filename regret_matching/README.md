# Regret Matching in Rock-Paper-Scissors

Regret Matching is a concept used in game theory to model adaptive strategies that learn from past actions. Let's apply it to the classic game of Rock-Paper-Scissors, where players repeatedly choose one of three possible actions—rock, paper, or scissors.

## The Idea

Regret Matching quantifies the regret associated with each action that a player could have taken but didn't. The central idea is that players learn by minimizing the regrets associated with their past actions. This approach helps players converge towards optimal strategies in repeated interactions.

## Rock-Paper-Scissors Example

Imagine a series of games of Rock-Paper-Scissors between two players. After each game, a player computes the regrets for their chosen action based on how other actions could have performed better. The player then updates their strategy to favor actions that have lower regrets.

## Counterfactual Regret Minimization (CFR)

Counterfactual Regret Minimization (CFR) is an extension of Regret Matching. It aims to find a strategy that minimizes the "counterfactual regret," which measures how much a player would regret not choosing an alternative action. CFR is particularly powerful in extensive-form games with imperfect information.

## How CFR Works

In CFR, a player considers all possible outcomes (counterfactuals) that could have occurred if they had chosen different actions in the past. The strategy is adjusted to minimize the total counterfactual regret across all these outcomes. Over iterations, the strategy converges towards a Nash equilibrium, where no player has an incentive to unilaterally deviate.

## Applications

Regret Matching and CFR have applications in various domains:

- **Poker**: CFR has been used to develop successful poker-playing bots, adapting strategies based on opponents' moves.
- **Algorithmic Trading**: The concepts are applied to model strategies that adapt to market dynamics.
- **Multi-Agent Systems**: CFR is valuable for developing adaptive agents in complex environments.

## Conclusion

Regret Matching and Counterfactual Regret Minimization provide powerful frameworks for learning adaptive strategies in repeated interactions and extensive-form games. By quantifying and minimizing regrets associated with actions, players converge towards strategies that optimize their outcomes over time. Understanding these concepts is essential for developing intelligent agents capable of adapting to dynamic scenarios.
