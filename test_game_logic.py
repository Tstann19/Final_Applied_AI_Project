from logic_utils import check_guess

## GUESS NUMBER GAME AUTOMATED TESTS
def test_winning_guess():
    # If the secret is 50 and guess is 50, it should be a win
    result = check_guess(50, 50)
    assert result == ("Win", "🎉 Correct!")

def test_guess_too_high():
    # If secret is 50 and guess is 60, hint should be "Too High"
    result = check_guess(60, 50)
    assert result == ("Too High", "📈 Go LOWER!")

def test_guess_too_low():
    # If secret is 50 and guess is 40, hint should be "Too Low"
    result = check_guess(40, 50)
    assert result == ("Too Low", "📉 Go HIGHER!")

def test_guess_edge_case_high():
    # If secret is 50 and guess is 51, hint should be "Too High"
    result = check_guess(51, 50)
    assert result == ("Too High", "📈 Go LOWER!")

def test_guess_edge_case_low():
    # If secret is 50 and guess is 49, hint should be "Too Low"
    result = check_guess(49, 50)
    assert result == ("Too Low", "📉 Go HIGHER!")

## GUESS POKE GAME AUTOMATED TESTS