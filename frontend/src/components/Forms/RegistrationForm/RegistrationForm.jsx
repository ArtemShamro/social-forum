import React, { use } from "react";
import Button from "../../Button/Button";
import classes from "./RegistrationForm.module.css";
import { useState } from "react";
import { Register, Login } from "../../../api/user";

export default function RegistrationForm({ closeModal }) {
  const [form, setForm] = useState({
    name: "",
    email: "",
    password: "",
    userType: "Customer",
    hasError: false,
  });

  function handleNameChange(event) {
    setForm((prev) => ({
      ...prev,
      name: event.target.value,
      hasError: event.target.value.trim().length == 0,
    }));
  }

  return (
    <section>
      <form className={classes.form_input}>
        <label htmlFor="registration">registration</label>

        <input
          type="text"
          placeholder="Name"
          value={form.name}
          onChange={handleNameChange}
          style={{
            border: form.hasError ? "1px solid red" : null,
          }}
        />

        <input
          type="email"
          placeholder="Email"
          value={form.email}
          onChange={(event) =>
            setForm((prev) => ({ ...prev, email: event.target.value }))
          }
        />

        <input
          type="password"
          placeholder="Password"
          value={form.password}
          onChange={(event) =>
            setForm((prev) => ({ ...prev, password: event.target.value }))
          }
        />

        <label htmlFor="type">Тип записи</label>
        <select
          id="reason"
          value={form.userType}
          onChange={(event) =>
            setForm((prev) => ({ ...prev, userType: event.target.value }))
          }
        >
          <option value="Customer">Покупатель</option>
          <option value="Business">Продавец</option>
        </select>

        {/* <pre>{JSON.stringify(form, null, 2)} </pre> */}
        <div className={classes.buttonContainer}>
          <Button
            className={classes.submitButton}
            onClick={(e) => {
              e.preventDefault(); // чтобы форма не перезагружала страницу
              Register({
                username: form.name,
                password: form.password,
                email: form.email,
              });
              Login({ username: form.name, password: form.password }).then(() =>
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
