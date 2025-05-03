import React, { use } from "react";
import Button from "../../Button/Button";
import classes from "./NewPostForm.module.css";
import { useState } from "react";
import { NewPost } from "../../../api/posts";

export default function RegistrationForm({ closeModal }) {
  const [form, setForm] = useState({
    title: "",
    description: "",
    private: false,
  });

  return (
    <section>
      <form className={classes.form_input}>
        <label htmlFor="New post">registration</label>

        <input
          type="text"
          placeholder="Title"
          value={form.title}
          onChange={(event) =>
            setForm((prev) => ({ ...prev, title: event.target.value }))
          }
          style={{
            border: form.hasError ? "1px solid red" : null,
          }}
        />

        <textarea
          placeholder="Description"
          value={form.description}
          onChange={(event) =>
            setForm((prev) => ({ ...prev, description: event.target.value }))
          }
          rows={20}
        />

        <label htmlFor="type">Тип записи</label>
        <select
          id="reason"
          value={form.private}
          onChange={(event) =>
            setForm((prev) => ({ ...prev, private: event.target.value }))
          }
        >
          <option value={false}>Публичный</option>
          <option value={true}>Приватный</option>
        </select>

        {/* <pre>{JSON.stringify(form, null, 2)} </pre> */}
        <div className={classes.buttonContainer}>
          <Button
            className={classes.submitButton}
            onClick={(e) => {
              e.preventDefault(); // чтобы форма не перезагружала страницу
              NewPost({
                title: form.title,
                description: form.description,
                is_private: form.private,
              }).then(() => window.location.reload());
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
