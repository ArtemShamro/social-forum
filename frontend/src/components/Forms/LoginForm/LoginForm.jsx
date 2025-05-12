import React, { use } from "react";
import Button from "../../Button/Button";
import classes from "./LoginForm.module.css";
import { useState } from "react";
import { Login } from "../../../api/user";

export default function LoginForm({ closeModal }) {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");

  return (
    <section>
      <form className={classes.form_input}>
        <label htmlFor="login">registration</label>

        <input
          type="text"
          placeholder="Name"
          value={username}
          onChange={(event) => setUsername(event.target.value)}
        />

        <input
          type="password"
          placeholder="Password"
          value={password}
          onChange={(event) => setPassword(event.target.value)}
        />
        <div className={classes.buttonContainer}>
          <Button
            className={classes.submitButton}
            onClick={(e) => {
              e.preventDefault(); // чтобы форма не перезагружала страницу
              Login({ username, password }).then(() =>
                window.location.reload()
              );
            }}
          >
            Отправить
          </Button>
          <Button className={classes.closeButton} onClick={closeModal}></Button>
        </div>
      </form>
    </section>
  );
}
