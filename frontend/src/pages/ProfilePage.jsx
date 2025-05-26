import React, { useState, useEffect, useContext } from "react";
import { useNavigate } from "react-router-dom";
import { AuthContext } from "../Context";
import { GetMe, UpdateUser } from "../api/user";
import { Form, Input, Button, Card, message, DatePicker } from "antd";
import dayjs from 'dayjs';
import styles from "./ProfilePage.module.css";

const ProfilePage = () => {
  const [userId, userName] = useContext(AuthContext);
  const [currentUserData, setCurrentUserData] = useState(null); // State to store full user data
  const [form] = Form.useForm();
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  useEffect(() => {
    if (!userId) {
      navigate("/");
      return;
    }
    loadUserData();
  }, [userId, navigate]); // Added navigate to dependency array

  const loadUserData = async () => {
    try {
      const userData = await GetMe();
      if (userData) {
        setCurrentUserData(userData); // Store full user data
      }
    } catch (error) {
      message.error("Failed to load user data");
      console.error("Failed to load user data:", error);
    }
  };

  const onFinish = async (values) => {
    setLoading(true);
    try {
      // Prepare data for update, only send fields that might be updated
      const updateData = {
        name: values.name,
        surname: values.surname,
        birthdate: values.birthdate ? values.birthdate.format('YYYY-MM-DD') : null, // Format date for backend
        mail: values.mail,
        phone: values.phone,
        // Only include password if it's not empty
        ...(values.password && { password: values.password }),
      };

      // Ensure we only send fields allowed by UserUpdate schema
      // (Assuming UserUpdate doesn't include login)
      const response = await UpdateUser(updateData);

      if (response) {
        message.success("Profile updated successfully");
        // Optionally reload user data after successful update
        loadUserData();
      } else {
         message.error("Update failed");
      }
    } catch (error) {
      message.error("Failed to update profile");
      console.error("Failed to update profile:", error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className={styles.container}>
      <Card title="Profile Settings" className={styles.card}>
         {/* Display static user info if currentUserData is available */}
         {currentUserData && (
           <div className={styles.staticInfo}>
             {/* <p><strong>User ID:</strong> {currentUserData.id}</p> */}
             {/* <p><strong>Login:</strong> {currentUserData.login}</p> */}
             <p><strong>Name:</strong> {currentUserData.name || 'N/A'}</p>
             <p><strong>Surname:</strong> {currentUserData.surname || 'N/A'}</p>
             <p><strong>Birthdate:</strong> {currentUserData.birthdate ? new Date(currentUserData.birthdate).toLocaleDateString() : 'N/A'}</p>
             <p><strong>Email:</strong> {currentUserData.mail}</p>
             <p><strong>Phone:</strong> {currentUserData.phone || 'N/A'}</p>
             <p><strong>Registered:</strong> {new Date(currentUserData.created_at).toLocaleDateString()}</p>
             <p><strong>Last Updated:</strong> {new Date(currentUserData.updated_at).toLocaleDateString()}</p>
             {/* Add other static fields like is_user, is_business if needed */}
           </div>
         )}
        <Form
          form={form}
          layout="vertical"
          onFinish={onFinish}
          className={styles.form}
        >
          <Form.Item
            label="Login (Username)"
            name="login" // Use 'login' to match backend and state
            rules={[{ required: false, message: "Please input your login!" }]}
            // Disable login field if it's not meant to be updated via this form
            // You can make this editable if your backend allows updating login via /auth/update
            disabled={true} 
          >
            <Input />
          </Form.Item>

          <Form.Item
            label="Email"
            name="mail" // Use 'mail' to match backend and state
            rules={[
              { type: "email", message: "Please enter a valid email!" },
            ]}
          >
            <Input />
          </Form.Item>
          
          <Form.Item
            label="First Name"
            name="name" // Use 'name' to match backend and state
            rules={[]}
          >
            <Input />
          </Form.Item>

          <Form.Item
            label="Surname"
            name="surname" // Use 'surname' to match backend and state
            rules={[]}
          >
            <Input />
          </Form.Item>

          <Form.Item
            label="Birthdate"
            name="birthdate" // Use 'birthdate' to match backend and state
          >
            {/* Use DatePicker for birthdate */}
            <DatePicker format="YYYY-MM-DD" />
          </Form.Item>

           <Form.Item
            label="Phone"
            name="phone" // Use 'phone' to match backend and state
            rules={[]}
          >
            <Input placeholder="+1234567890" />{/* Add placeholder for format hint*/}
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
