# Token types
#
# EOF (end-of-file) token is used to indicate that
# there is no more input left for lexical analysis
INTEGER, PLUS, MINUS, SPACE, EOF = 'INTEGER', 'PLUS', 'MINUS', 'SPACE', 'EOF'


class Token(object):
    def __init__(self, type, value):
        # token type: INTEGER, PLUS, or EOF
        self.type = type
        # token value: 0, 1, 2. 3, 4, 5, 6, 7, 8, 9, '+', or None
        self.value = value

    def __str__(self):
        """String representation of the class instance.

        Examples:
            Token(INTEGER, 3)
            Token(PLUS '+')
        """
        return 'Token({type}, {value})'.format(
            type=self.type,
            value=repr(self.value)
        )

    def __repr__(self):
        return self.__str__()


class Interpreter(object):
    def __init__(self, text):
        # client (user) string input, e.g. "3+5"
        self.text = text
        # self.pos is an index into self.text
        self.pos = 0
        # current token instance
        self.current_token = None

    def error(self):
        raise Exception('Error parsing input')

    def get_next_token(self):
        """Lexical analyzer (also known as scanner or tokenizer)

        This method is responsible for breaking a sentence
        apart into tokens. One token at a time.
        """
        text = self.text

        # is self.pos index past the end of the self.text ?
        # if so, then return EOF token because there is no more
        # input left to convert into tokens
        if self.pos > len(text) - 1:
            return Token(EOF, None)

        # get a character at the position self.pos and decide
        # what token to create based on the single character
        current_char = text[self.pos]

        # if the character is a digit then convert it to
        # integer, create an INTEGER token, increment self.pos
        # index to point to the next character after the digit,
        # and return the INTEGER token
        if current_char.isdigit():
            token = Token(INTEGER, current_char)
            self.pos += 1
            return token

        if current_char.isspace():
            token = Token(SPACE, current_char)
            self.pos += 1
            return token

        if current_char == '+':
            token = Token(PLUS, current_char)
            self.pos += 1
            return token

        if current_char == '-':
            token = Token(MINUS, current_char)
            self.pos += 1
            return token

        self.error()

    def eat(self, token_type):
        # compare the current token type with the passed token
        # type (token_type). If they match then "eat" (meaning confirm)
        # the current token, otherwise raise an exception.
        if self.current_token.type == token_type:
            pass
        else:
            self.error()

    def expr(self):
        """expr -> Responsible for finding the 'INTEGER MINUS INTEGER' sequence"""
        # 1- Find operator (MINUS) in user input
        op_index = self.text.find('-')
        if op_index == -1:
            self.error()

        # 2- Grab left operand. We expect single or multiple 
        # digits integers (with possible whitespace)
        left = Token(INTEGER, '')
        for _ in range(self.pos, op_index):
            # set current token to the first token taken from the input
            self.current_token = self.get_next_token()
            if(self.current_token.type == SPACE):
                continue
            left.value += self.current_token.value
        
        # 3- Grab operator sign
        self.current_token = self.get_next_token()
        operator = self.current_token
        self.eat(MINUS)

        # 4- Grab right operand. We expect single or multiple 
        # digits integers (with possible whitespace)
        right = Token(INTEGER, '')

        for _ in range(self.pos, len(self.text)):
            self.current_token = self.get_next_token()
            if(self.current_token.type == SPACE):
                continue
            right.value += self.current_token.value
        
        # after the above call the self.current_token is set to
        # EOF token

        # at this point INTEGER MINUS INTEGER sequence of tokens
        # has been successfully found and the method can just
        # return the result of adding two integers, thus
        # effectively interpreting client input

        result = int(left.value) - int(right.value)
        return result


def main():
    while True:
        try:
            text = input('kassi calc> ')
        except EOFError:
            break
        if not text:
            continue
        interpreter = Interpreter(text)
        result = interpreter.expr()
        print(result)


if __name__ == '__main__':
    main()
