import unittest

from src.lab3.sudoku import (
    get_col, get_row, group, get_block, find_empty_positions,
    find_possible_values, solve, check_solution, generate_sudoku
)


class SudokuTestCase(unittest.TestCase):
    def test_group(self):
        self.assertEqual(group([1, 2, 3, 4], 2), [[1, 2], [3, 4]])
        self.assertEqual(group([1, 2, 3, 4, 5, 6, 7, 8, 9], 3), [[1, 2, 3], [4, 5, 6], [7, 8, 9]])
        with self.assertRaises(ValueError):
            group([1, 2, 3, 4], -1)

    def test_get_row(self):
        self.assertEqual(get_row([['1', '2', '.'], ['4', '5', '6'], ['7', '8', '9']], (0, 0)), ['1', '2', '.'])
        self.assertEqual(get_row([['1', '2', '3'], ['4', '.', '6'], ['7', '8', '9']], (1, 0)), ['4', '.', '6'])
        self.assertEqual(get_row([['1', '2', '3'], ['4', '5', '6'], ['.', '8', '9']], (2, 0)), ['.', '8', '9'])
        with self.assertRaises(IndexError):
            get_row([['1', '2', '3'], ['4', '5', '6'], ['.', '8', '9']], (-2, 0))

    def test_get_col(self):
        self.assertEqual(get_col([['1', '2', '.'], ['4', '5', '6'], ['7', '8', '9']], (0, 0)), ['1', '4', '7'])
        self.assertEqual(get_col([['1', '2', '3'], ['4', '.', '6'], ['7', '8', '9']], (0, 1)), ['2', '.', '8'])
        self.assertEqual(get_col([['1', '2', '3'], ['4', '5', '6'], ['.', '8', '9']], (0, 2)), ['3', '6', '9'])
        with self.assertRaises(IndexError):
            get_col([['1', '2', '3'], ['4', '5', '6'], ['.', '8', '9']], (0, -2))

    def test_get_block(self):
        grid = [
            ["5", "3", ".", ".", "7", ".", ".", ".", "."],
            ["6", ".", ".", "1", "9", "5", ".", ".", "."],
            [".", "9", "8", ".", ".", ".", ".", "6", "."],
            ["8", ".", ".", ".", "6", ".", ".", ".", "3"],
            ["4", ".", ".", "8", ".", "3", ".", ".", "1"],
            ["7", ".", ".", ".", "2", ".", ".", ".", "6"],
            [".", "6", ".", ".", ".", ".", "2", "8", "."],
            [".", ".", ".", "4", "1", "9", ".", ".", "5"],
            [".", ".", ".", ".", "8", ".", ".", "7", "9"],
        ]
        self.assertEqual(get_block(grid, (0, 1)), ['5', '3', '.', '6', '.', '.', '.', '9', '8'])
        self.assertEqual(get_block(grid, (4, 7)), ['.', '.', '3', '.', '.', '1', '.', '.', '6'])
        self.assertEqual(get_block(grid, (8, 8)), ['2', '8', '.', '.', '.', '5', '.', '7', '9'])
        with self.assertRaises(IndexError):
            get_block(grid, (-4, 7))
        with self.assertRaises(IndexError):
            get_block(grid, (4, -7))

    def test_find_empty_positions(self):
        self.assertEqual(find_empty_positions([['1', '2', '.'], ['4', '5', '6'], ['7', '8', '9']]), (0, 2))
        self.assertEqual(find_empty_positions([['1', '2', '3'], ['4', '.', '6'], ['7', '8', '9']]), (1, 1))
        self.assertEqual(find_empty_positions([['1', '2', '3'], ['4', '5', '6'], ['.', '8', '9']]), (2, 0))
        self.assertEqual(find_empty_positions([['1', '2', '3'], ['4', '5', '6'], ['7', '8', '9']]), None)
        self.assertEqual(find_empty_positions([['1', '2', '.'], ['4', '5', '6'], ['.', '8', '9']]), (0, 2))
        self.assertEqual(find_empty_positions([['.', '.', '.'], ['.', '.', '.'], ['.', '.', '.']]), (0, 0))

    def test_find_possible_values(self):
        grid = [
            ["5", "3", ".", ".", "7", ".", ".", ".", "."],
            ["6", ".", ".", "1", "9", "5", ".", ".", "."],
            [".", "9", "8", ".", ".", ".", ".", "6", "."],
            ["8", ".", ".", ".", "6", ".", ".", ".", "3"],
            ["4", ".", ".", "8", ".", "3", ".", ".", "1"],
            ["7", ".", ".", ".", "2", ".", ".", ".", "6"],
            [".", "6", ".", ".", ".", ".", "2", "8", "."],
            [".", ".", ".", "4", "1", "9", ".", ".", "5"],
            [".", ".", ".", ".", "8", ".", ".", "7", "9"],
        ]
        self.assertEqual(find_possible_values(grid, (0, 2)), {'1', '2', '4'})
        self.assertEqual(find_possible_values(grid, (4, 7)), {'2', '5', '9'})

    def test_solve(self):
        grid = [
            ["5", "3", ".", ".", "7", ".", ".", ".", "."],
            ["6", ".", ".", "1", "9", "5", ".", ".", "."],
            [".", "9", "8", ".", ".", ".", ".", "6", "."],
            ["8", ".", ".", ".", "6", ".", ".", ".", "3"],
            ["4", ".", ".", "8", ".", "3", ".", ".", "1"],
            ["7", ".", ".", ".", "2", ".", ".", ".", "6"],
            [".", "6", ".", ".", ".", ".", "2", "8", "."],
            [".", ".", ".", "4", "1", "9", ".", ".", "5"],
            [".", ".", ".", ".", "8", ".", ".", "7", "9"],
        ]
        expected_solution = [
            ["5", "3", "4", "6", "7", "8", "9", "1", "2"],
            ["6", "7", "2", "1", "9", "5", "3", "4", "8"],
            ["1", "9", "8", "3", "4", "2", "5", "6", "7"],
            ["8", "5", "9", "7", "6", "1", "4", "2", "3"],
            ["4", "2", "6", "8", "5", "3", "7", "9", "1"],
            ["7", "1", "3", "9", "2", "4", "8", "5", "6"],
            ["9", "6", "1", "5", "3", "7", "2", "8", "4"],
            ["2", "8", "7", "4", "1", "9", "6", "3", "5"],
            ["3", "4", "5", "2", "8", "6", "1", "7", "9"],
        ]
        self.assertEqual(solve(grid), expected_solution)

    def test_check_solution(self):
        correct_solution = [
            ["5", "3", "4", "6", "7", "8", "9", "1", "2"],
            ["6", "7", "2", "1", "9", "5", "3", "4", "8"],
            ["1", "9", "8", "3", "4", "2", "5", "6", "7"],
            ["8", "5", "9", "7", "6", "1", "4", "2", "3"],
            ["4", "2", "6", "8", "5", "3", "7", "9", "1"],
            ["7", "1", "3", "9", "2", "4", "8", "5", "6"],
            ["9", "6", "1", "5", "3", "7", "2", "8", "4"],
            ["2", "8", "7", "4", "1", "9", "6", "3", "5"],
            ["3", "4", "5", "2", "8", "6", "1", "7", "9"],
        ]
        block_incorrect_solution = [
            ["5", "5", "4", "6", "7", "8", "9", "1", "2"],
            ["6", "7", "2", "1", "9", "5", "3", "4", "8"],
            ["1", "9", "8", "3", "4", "2", "5", "6", "7"],
            ["8", "5", "9", "7", "6", "1", "4", "2", "3"],
            ["4", "2", "6", "8", "5", "3", "7", "9", "1"],
            ["7", "1", "3", "9", "2", "4", "8", "5", "6"],
            ["9", "6", "1", "5", "3", "7", "2", "8", "4"],
            ["2", "8", "7", "4", "1", "9", "6", "3", "5"],
            ["3", "4", "5", "2", "8", "6", "1", "7", "9"],
        ]
        row_incorrect_solution = [
            ["5", "3", "4", "5", "7", "8", "9", "1", "2"],
            ["6", "7", "2", "1", "9", "5", "3", "4", "8"],
            ["1", "9", "8", "3", "4", "2", "5", "6", "7"],
            ["8", "5", "9", "7", "6", "1", "4", "2", "3"],
            ["4", "2", "6", "8", "5", "3", "7", "9", "1"],
            ["7", "1", "3", "9", "2", "4", "8", "5", "6"],
            ["9", "6", "1", "5", "3", "7", "2", "8", "4"],
            ["2", "8", "7", "4", "1", "9", "6", "3", "5"],
            ["3", "4", "5", "2", "8", "6", "1", "7", "9"],
        ]
        column_incorrect_solution = [
            ["5", "3", "4", "6", "7", "8", "9", "1", "2"],
            ["6", "7", "2", "1", "9", "5", "3", "4", "8"],
            ["1", "9", "8", "3", "4", "2", "5", "6", "7"],
            ["5", "5", "9", "7", "6", "1", "4", "2", "3"],
            ["4", "2", "6", "8", "5", "3", "7", "9", "1"],
            ["7", "1", "3", "9", "2", "4", "8", "5", "6"],
            ["9", "6", "1", "5", "3", "7", "2", "8", "4"],
            ["2", "8", "7", "4", "1", "9", "6", "3", "5"],
            ["3", "4", "5", "2", "8", "6", "1", "7", "9"],
        ]
        self.assertEqual(check_solution(correct_solution), True)
        self.assertEqual(check_solution(block_incorrect_solution), False)
        self.assertEqual(check_solution(row_incorrect_solution), False)
        self.assertEqual(check_solution(column_incorrect_solution), False)

    def test_generate_sudoku(self):
        # 40 заполненных позиций
        grid = generate_sudoku(40)
        empty_positions = sum(1 for row in grid for e in row if e == '.')
        self.assertEqual(empty_positions, 41)
        solution = solve(grid)
        self.assertIsNotNone(solution)
        self.assertTrue(check_solution(solution))

        # 81 заполненная позиция
        grid = generate_sudoku(81)
        empty_positions = sum(1 for row in grid for e in row if e == '.')
        self.assertEqual(empty_positions, 0)
        solution = solve(grid)
        self.assertIsNotNone(solution)
        self.assertTrue(check_solution(solution))

        # 0 заполненных позиций
        grid = generate_sudoku(0)
        empty_positions = sum(1 for row in grid for e in row if e == '.')
        self.assertEqual(empty_positions, 81)
        solution = solve(grid)
        self.assertIsNotNone(solution)
        self.assertTrue(check_solution(solution))

        # 1000 заполненных позиций
        grid = generate_sudoku(1000)
        empty_positions = sum(1 for row in grid for e in row if e == '.')
        self.assertEqual(empty_positions, 0)
        solution = solve(grid)
        self.assertIsNotNone(solution)
        self.assertTrue(check_solution(solution))
