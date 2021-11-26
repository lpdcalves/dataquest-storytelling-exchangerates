from data_story_teller import DataStoryTeller

data_story_teller = DataStoryTeller()


def test_read_data():
    data_story_teller.read_data()
    assert (data_story_teller.exchange_rates.empty == False)
