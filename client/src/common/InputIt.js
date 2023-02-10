import React, { useState } from "react";
import { useNavigate } from "react-router-dom";

function InputIt({
    token,
    setToken,
    randomNumber,
    setRandomNumber,
    email,
    setEmail,
}) {
    const [token_inp, setToken_inp] = useState("");
    const [rand_inp, setRand_inp] = useState("");
    const [email_inp, setEmail_inp] = useState("");

    const navigate = useNavigate();

    let handle = () => {
        console.log("token", token);
        console.log("randomNumber", randomNumber);
    };
    return (
        <>
            <div style={{ margin: "20px" }}>
                <div>Token Value</div>
                <input
                    value={token_inp}
                    onChange={(e) => setToken_inp(e.target.value)}
                    type="text"
                ></input>
                <button
                    className="jj_stats_button"
                    onClick={(e) => setToken(token_inp)}
                >
                    {" "}
                    Set{" "}
                </button>
                <br></br>
                <br></br>
                <br></br>
                <div>Random value</div>
                <input
                    value={rand_inp}
                    onChange={(e) => setRand_inp(e.target.value)}
                    type="text"
                ></input>
                <button
                    className="jj_stats_button"
                    onClick={(e) => setRandomNumber(token_inp)}
                >
                    Set
                </button>

                <br></br>
                <br></br>
                <div>Email</div>
                <input
                    value={email_inp}
                    onChange={(e) => setEmail_inp(e.target.value)}
                    type="text"
                ></input>
                <button
                    className="jj_stats_button"
                    onClick={(e) => setEmail(token_inp)}
                >
                    Set
                </button>
            </div>

            <button
                className="jj_stats_button"
                onClick={(e) => navigate("/warehouse/", { replace: true })}
            >
                warehouse{" "}
            </button>

            <button
                className="jj_stats_button"
                onClick={(e) => navigate("/rider/maps", { replace: true })}
            >
                rider{" "}
            </button>
        </>
    );
}

export default InputIt;
