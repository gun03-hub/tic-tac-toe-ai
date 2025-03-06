import React, { useState } from "react";
import "./TicTacToe.css"; // Import new CSS

const TicTacToe = () => {
  const [board, setBoard] = useState([
    ["", "", ""],
    ["", "", ""],
    ["", "", ""]
  ]);
  const [winner, setWinner] = useState(null);
  const [score, setScore] = useState({ X: 0, O: 0 });

  const handleClick = async (row, col) => {
    if (board[row][col] !== "" || winner) return;

    const newBoard = board.map((r, i) =>
      r.map((cell, j) => (i === row && j === col ? "X" : cell))
    );

    setBoard(newBoard);

    const response = await fetch("http://127.0.0.1:5000/ai-move", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ board: newBoard }),
    });

    const data = await response.json();
    setBoard(data.board);
    setWinner(data.winner);

    if (data.winner) {
      setScore((prevScore) => ({
        ...prevScore,
        [data.winner]: prevScore[data.winner] + 1,
      }));
    }
  };

  const resetGame = () => {
    setBoard([
      ["", "", ""],
      ["", "", ""],
      ["", "", ""]
    ]);
    setWinner(null); // Reset winner state
  };

  return (
    <div>
      <h1>Tic Tac Toe</h1>

      <div className="scoreboard">
        <div className="score">X Wins: {score.X}</div>
        <div className="score">O Wins: {score.O}</div>
      </div>

      <div className="board">
        {board.map((row, i) =>
          row.map((cell, j) => (
            <div key={`${i}-${j}`} className={`cell ${cell}`} onClick={() => handleClick(i, j)}>
              {cell}
            </div>
          ))
        )}
      </div>

      {winner && <p className="status">{winner === "Draw" ? "It's a Draw!" : `Winner: ${winner}`}</p>}
      
      <button className="reset-button" onClick={resetGame}>
        Reset Game
      </button>
    </div>
  );
};

export default TicTacToe;
