# DAILY TRANSACTIONS MANAGEMENT SYSTEM

## TARGETED FOR FINANCIAL AGENTS

## Screenshots

| Screenshot | Screenshot |
|------------|------------|
| ![14](https://github.com/user-attachments/assets/ed69de88-6362-4646-a141-ac93cf8d40ec) | ![5](https://github.com/user-attachments/assets/0d5eb0d2-7ca2-4f5a-a936-eb6a09858892) |
| ![screenshot_2](https://github.com/user-attachments/assets/66ad8240-4167-4507-bf58-faf485f92d8f) | ![screenshot_1](https://github.com/user-attachments/assets/720097eb-bc05-4b19-999d-56771d398fef) |

**Live Demo:** [View the Live Demo](https://transactionmis.pythonanywhere.com/)
Login username:  demo
password: demo1234

## 1. Introduction
The Daily Transactions Management System is designed to facilitate the recording and management of financial transactions conducted by agents. This web-based application enables agents to efficiently handle money transfers and withdrawals while simultaneously sending SMS notifications to customers to confirm the completion of their transactions. This project uses an SMS API, but you must use your own SMS API provided by the telecom company. The system includes the following key features:

| Feature | Description |
|---------|-------------|
| **SMS feedback to customer** | Once a record is added, deleted, or updated, the customer will be notified via SMS. |
| **Realtime Transaction analytics** | Analytics available daily, weekly, monthly, annually, and lifetime for transaction records. |
| **Add, Delete, Update transaction** | Full functionality for managing transactions, including adding new records, deleting existing ones, and updating transaction details. |
| **View Transactions** | Agents can view all transactions with the ability to filter and sort records as needed. |

## 2. Problem Statement
The target audience for this project includes financial agents, especially in Africa, who handle daily transactions and their customers who expect timely and accurate information about their financial activities. The existing methods for tracking transactions are often manual and prone to errors, leading to delays and miscommunication. Additionally, customers frequently lack immediate updates on their transaction statuses, which can lead to dissatisfaction and distrust in financial services.

## 3. Importance of Project
The importance of this project is illustrated through the following benefits:

| Benefit | Description |
|---------|-------------|
| **Efficiency** | Reduces the time agents spend on manual entry and follow-ups. |
| **Accuracy** | Minimizes the risk of human error in transaction records. |
| **Customer Satisfaction** | Provides customers with immediate feedback, improving their trust and engagement with the service. |
| **Data Security** | Protects sensitive transaction data through secure storage and access protocols. |

## 4. Main Objective
The main objective of the Daily Transactions Management System is to develop a comprehensive web application that:
- Accurately records daily financial transactions performed by agents (both sending money and withdrawals).
- Sends immediate SMS notifications to customers to confirm the successful completion of their transactions.
- Offers a user-friendly interface for both agents and customers.

## 5. SPECIFIC OBJECTIVES
To achieve the main objective, the project includes the following specific goals:

| Specific Objective | Description |
|-------------------|-------------|
| **User Interface Design** | Create an intuitive and responsive UI for agents to input transaction data effortlessly. |
| **Transaction Handling** | Implement backend logic to handle transaction processing and storage securely. |
| **SMS Integration** | Utilize a third-party SMS API to send real-time notifications to customers upon transaction completion. |
| **Data Reporting** | Develop functionality for generating daily and monthly transaction reports to aid agents in tracking performance. |
| **Error Handling** | Ensure robust error handling and logging mechanisms for troubleshooting and maintaining system integrity. |

## 6. Design Methodology
### Technologies Used

| Technology | Description |
|------------|-------------|
| **Backend** | **Django**: A high-level Python web framework for rapid development and clean design. |
| **Frontend** | **HTML**: For structuring web pages.<br>**Bootstrap**: For responsive design and UI components.<br>**JavaScript**: For enhancing user interactions and functionalities. |
| **Database** | **MySQL**: A relational database for storing transaction records and user data. |
| **SMS Service** | A RESTful API for sending SMS notifications. |

### Development Approach

| Approach | Description |
|----------|-------------|
| **Agile Methodology** | The project will follow an agile development approach, allowing for iterative progress and feedback from stakeholders. |
| **MVC Architecture** | Utilizing the Model-View-Controller (MVC) pattern to separate concerns within the application, facilitating easier maintenance and scalability. |
| **Version Control** | Using Git for version control to track changes and collaborate effectively. |

## 7. Conclusions and Future Work
The Daily Transactions Management System provides a solid foundation for managing financial transactions effectively, addressing both operational efficiency and customer communication needs.

### Future Enhancements

| Enhancement | Description |
|-------------|-------------|
| **User Authentication** | Implementing a secure user authentication system to protect sensitive data. |
| **Payment Gateway Integration** | Adding support for various payment methods, including credit/debit cards and mobile money. |
| **Analytics Dashboard** | Developing an analytics dashboard for agents to visualize transaction trends and customer behaviors. |
| **Mobile Application** | Creating a mobile app version of the system to enhance accessibility for agents on the go. |
| **Integration with Telecom Companies' API** | Integrating the system with telecom companies' API for transactions to streamline operations further. |

This project not only streamlines transaction management but also paves the way for more advanced financial services in the future.
