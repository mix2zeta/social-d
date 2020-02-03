import fix_csv
import pytest

@pytest.mark.filterwarnings('ignore:\'U\' mode is deprecated')
def test_read_csv():
    fix_csv.read_csv()