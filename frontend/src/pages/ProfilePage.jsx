import React, { useState, useEffect, useContext } from "react";
import { useNavigate } from "react-router-dom";
import { AuthContext } from "../Context";
import { GetMe, UpdateUser } from "../api/user";
import { Form, Input, Button, Card, message } from "antd";
import styles from "./ProfilePage.module.css";

const ProfilePage = () => {
  const [userId, userName] = useContext(AuthContext);
  const [form] = Form.useForm();
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  useEffect(() => {
    if (!userId) {
      navigate("/");
      return;
    }
    loadUserData();
  }, [userId]);

  const loadUserData = async () => {
    try {
      const userData = await GetMe();
      if (userData) {
        form.setFieldsValue({
          username: userData.login,
          email: userData.mail,
        });
      }
    } catch (error) {
      message.error("Failed to load user data");
    }
  };

  const onFinish = async (values) => {
    setLoading(true);
    try {
      const response = await UpdateUser({
        login: values.username,
        mail: values.email,
        password: values.password, // Only if provided
      });

      if (response) {
        message.success("Profile updated successfully");
      }
    } catch (error) {
      message.error("Failed to update profile");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className={styles.container}>
      <Card title="Profile Settings" className={styles.card}>
        <Form
          form={form}
          layout="vertical"
          onFinish={onFinish}
          className={styles.form}
        >
          <Form.Item
            label="Username"
            name="username"
            rules={[{ required: true, message: "Please input your username!" }]}
          >
            <Input />
          </Form.Item>

          <Form.Item
            label="Email"
            name="email"
            rules={[
              { required: true, message: "Please input your email!" },
              { type: "email", message: "Please enter a valid email!" },
            ]}
          >
            <Input />
          </Form.Item>

          <Form.Item
            label="New Password"
            name="password"
            rules={[
              { min: 6, message: "Password must be at least 6 characters!" },
            ]}
          >
            <Input.Password placeholder="Leave blank to keep current password" />
          </Form.Item>

          <Form.Item>
            <Button type="primary" htmlType="submit" loading={loading}>
              Update Profile
            </Button>
          </Form.Item>
        </Form>
      </Card>
    </div>
  );
};

export default ProfilePage;
