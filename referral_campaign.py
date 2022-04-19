"""Referral campaign."""

from typing import List, NamedTuple, Optional

User = NamedTuple(
    "User",
    [
        ("user_name", str),
        ("code", str),
        ("referral_code", Optional[str]),
    ],
)

ReferralLayer = NamedTuple(
    "ReferralLayer",
    [
        ("number_of_referrers", int),
        ("number_of_referees", int),
    ],
)


class ReferralUser:
    """
    User in a referral campaign.

    :param user_name: user name
    :param code: code
    :param referral_code: referral code
    """

    def __init__(
        self,
        user_name: str,
        code: str,
        referral_code: Optional[str],
    ):
        self.user_name = user_name
        self.code = code
        self.referral_code = referral_code
        self.child: List[ReferralUser] = []

    @property
    def get_max_depth(self) -> int:
        """
        Get maximum depth of referee for a referrer.

        :return: user's maximum depth
        """
        max_depth = 0

        for child in self.child:
            child_depth = child.get_max_depth
            if max_depth < child_depth:
                max_depth = child_depth

        return max_depth + 1

    @property
    def referral_layers(self) -> List[ReferralLayer]:
        """
        Get number of referrers and number of referees for each layer.

        :return: list of layers with numbers of referrers and referees
        """
        layers = []
        nodes = [self]

        while len(nodes) > 0:
            nodes_length = len(nodes)
            referrers = 0
            referees = 0

            while nodes_length > 0:
                node = nodes[0]
                nodes.pop(0)
                number_child = len(node.child)

                if number_child > 0:
                    referrers += 1
                    referees += number_child

                for i in range(number_child):
                    nodes.append(node.child[i])
                nodes_length -= 1

            layers.append(ReferralLayer(referrers, referees))

        return layers[:-1]


def convert_to_referral_users(users: List[User]) -> List[ReferralUser]:
    """
    Convert a list of tuple users to a list of class users.

    :param users: list of  user
    :return: list of class users
    """
    referral_users = [
        ReferralUser(user.user_name, user.code, user.referral_code) for user in users
    ]

    for referrer in referral_users:
        for referee in referral_users:
            if referrer.code == referee.referral_code:
                referrer.child.append(referee)

    return referral_users


def get_longest_length_sequences(referral_users: List[ReferralUser]) -> int:
    """
    Get the longest length of referral sequences.

    :param referral_users: list of  referral users
    :return: the longest length of referral sequences
    """
    max_roots_depths = [
        referral_user.get_max_depth
        for referral_user in referral_users
        if referral_user.referral_code is None
    ]

    return max(max_roots_depths) - 1


def get_numbers_of_referrers_referees(
    referral_users: List[ReferralUser], max_depth: int
) -> List[ReferralLayer]:
    """
    Get numbers of referrers and number of referees for all layers.

    :param referral_users: list of  referral users
    :param max_depth: the longest length of referral sequences
    :return: list of layers with numbers of referrers and referees
    """
    total_referral_layers = []

    for i in range(max_depth):
        referrers = 0
        referees = 0
        for referral_user in referral_users:
            if not referral_user.referral_code and len(referral_user.child) > 0:
                if len(referral_user.referral_layers) > i:
                    referrers += referral_user.referral_layers[i].number_of_referrers
                    referees += referral_user.referral_layers[i].number_of_referees

        total_referral_layers.append(ReferralLayer(referrers, referees))

    return total_referral_layers


if __name__ == "__main__":
    """Lets create below referral trees
    Layer 1:                   A                                     L                   S
                             / |  \                                /   \
    Layer 2:                B  C    D                             M     N
                           / \    / | | \                       / | \   |
    Layer 3:              E  F   H  G I J                      Q  O  P  R
                                    |
    Bottom Layer:                   K
    """

    users = [
        User("A", "a_code", None),
        User("B", "b_code", "a_code"),
        User("C", "c_code", "a_code"),
        User("D", "d_code", "a_code"),
        User("E", "e_code", "b_code"),
        User("F", "f_code", "b_code"),
        User("G", "g_code", "d_code"),
        User("H", "h_code", "d_code"),
        User("I", "i_code", "d_code"),
        User("J", "j_code", "d_code"),
        User("K", "k_code", "g_code"),
        User("L", "l_code", None),
        User("M", "m_code", "l_code"),
        User("N", "n_code", "l_code"),
        User("O", "o_code", "m_code"),
        User("P", "p_code", "m_code"),
        User("Q", "q_code", "m_code"),
        User("R", "r_code", "n_code"),
        User("S", "s_code", None),
    ]

    referral_users = convert_to_referral_users(users)

    max_depth = get_longest_length_sequences(referral_users)
    print(f"The longest length of all sequences: {max_depth}")

    layers_referrers_referees = get_numbers_of_referrers_referees(
        referral_users, max_depth
    )
    for index, referral_layer in enumerate(layers_referrers_referees):
        print(
            f"Layer {index+1} has {referral_layer.number_of_referrers} "
            f"referrers and {referral_layer.number_of_referees} referees"
        )

    """
    The longest length of all sequences: 3
    Layer 1 has 2 referrers and 5 referees
    Layer 2 has 4 referrers and 10 referees
    Layer 3 has 1 referrers and 1 referees
    """
    # Bottom layer always has 0 referrer and 0 referee, so I exclude it from the output
