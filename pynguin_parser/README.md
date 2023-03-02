# Pynguin Test Case Parser and Transformer

Programs useful to tansform Pynguin test cases on executable ones.

Pynguin presents a behaviour when creating test cases automatically, when a test case did not present a correct behaiour, by default, Pynguin includes in such a test an annotation like the example below:

```python
@pytest.mark.xfail(strict=True)
def test_case_5():
    str_0 = "e6ic|mE"
    identifier_0 = module_0.Identifier()
    var_0 = identifier_0.validateIdentifier(str_0)
    assert var_0 is False
    str_1 = "f"
    var_1 = identifier_0.validateIdentifier(str_1)
    assert var_1 is True
    var_0.validateIdentifier(var_1)
```

This annotation indicates that this test has a problem and must fail during test execution.

The problem is always with the last statement in the test method. In this way, the tc_tranformer.py changes `@pytest.mark.xfail(strict=True)` to `@pytest.mark.xfail(strict=False)`, and also removes the last statement of test method. In this way, we can run this test outside Pynguin system without test case indicates test failures.

## How to run

```bash
python tc_transformer.py test.py
```

### Output for the same test case above

```python
@pytest.mark.xfail(strict=False)
def test_case_5():
    str_0 = "e6ic|mE"
    identifier_0 = module_0.Identifier()
    var_0 = identifier_0.validateIdentifier(str_0)
    assert var_0 is False
    str_1 = "f"
    var_1 = identifier_0.validateIdentifier(str_1)
    assert var_1 is True
```

## Combining parser programs to generate a subset of a test test set

```
python tc_list.py ../../binarySearchTree1/MIO/test_binarySearchTree1_MIO.py | xargs ./tc_list_reordered.py 8 5 | xargs ./tc_subset.py ../../binarySearchTree1/MIO/test_binarySearchTree1_MIO.py 
```