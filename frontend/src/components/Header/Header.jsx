import React, { useEffect, useContext } from "react";
import RegistredUserBlock from "./RegistrationBlock/RegistredUserBlock";
import UnregistredUserBlock from "./RegistrationBlock/UnregistredUserBlock";
import { useState } from "react";
import "./Header.css";
import { AuthContext } from "../../Context";
import { useNavigate } from "react-router-dom";

export default function Header() {
  const [now, setNow] = useState(new Date());
  const [userId, userName] = useContext(AuthContext);
  const router = useNavigate();

  useEffect(() => {
    const interval = setInterval(() => {
      setNow(new Date());
    }, 1000);
    return () => clearInterval(interval);
  }, []);

  return (
    <header>
      <h3 onClick={() => router("/", { replace: true })}>My new header</h3>

      <span>
        {!userId && <UnregistredUserBlock />}
        {userId && <RegistredUserBlock />}
      </span>
    </header>
  );
}
