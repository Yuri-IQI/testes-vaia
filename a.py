class TreeNode:
    def __init__(self, type, content, left=None, right=None):
        self.type = type
        self.content = content
        self.left = left
        self.right = right

    def answer(self, choice):
        if self.type != 'QUESTION':
            return None
        
        if choice == 's':
            return self.left
        elif choice == 'n':
            return self.right
        
        return None


def run_tree(node):
    while node.type == 'QUESTION':
        resposta = input(node.content + " (s/n): ").lower()
        node = node.answer(resposta)
    
    print("Sugestão:", node.content)


arvore = TreeNode(
    'QUESTION', "Você quer algo doce?",
    left=TreeNode(
        'QUESTION', "Você quer uma bebida?",
        left=TreeNode('RESULT', "Suco"),
        right=TreeNode('RESULT', "Sorvete")
    ),
    right=TreeNode(
        'QUESTION', "Você quer algo rápido?",
        left=TreeNode('RESULT', "Hambúrguer"),
        right=TreeNode('RESULT', "Pizza")
    )
)

run_tree(arvore)