# Benchmark_Circuits
[![MIT License](https://img.shields.io/badge/License-MIT-green.svg)](https://choosealicense.com/licenses/mit/)
This repository is dedicated to a powerful and user-friendly framework designed for testing various circuits using Circom. Our main objective is to simplify the testing process, allowing developers to easily add new circuits and conduct reliable tests.

**Key features of the framework:**

1.  **Extensibility:** The framework is highly extensible. To add new circuits, simply follow a few clear rules and place the circuits in the `circuits/base` folder. Additionally, provide a commented `main` file following the appropriate formatting.
    
2.  **Easy Customization:** You can effortlessly customize circuit values using Python. Just make the necessary changes in the test files within the `circuits` directory to update the circuit name, powersoftau, and other relevant parameters.
    

**Getting Started:**

1.  Clone this repository to your local system.
2.  Add new circuits to the `circuits/base` folder.
3.  Modify the `main` file of the circuit with the correct formatting and values to be customized in Python.
4.  Edit the test files in the `circuits` directory to adapt them to the new circuit, updating the circuit name, powersoftau, and other parameters as needed.
5.  Run the tests to ensure the circuit functions correctly.

**Running Tests:**

After conducting tests using this framework, you can analyze the following metrics:

| Circuit Name           | Input Size | Number of Constraints | Time to Compile & Generate Witness | Memory to Compile & Generate Witness | Time to Setup Proof | Memory to Setup Proof | Time to Generate Proof | Memory to Generate Proof | Time to Verify Proof | Memory to Verify Proof |
|------------------------|------------|-----------------------|-----------------------------------|---------------------------------------|--------------------|--------------------|-----------------------|---------------------------|--------------------|--------------------|
| Sample Circuit 1       | 256 bits   | 100,000               | 3.5 seconds                       | 500 MB                                | 1.2 seconds        | 300 MB            | 2.8 seconds           | 400 MB                    | 0.5 seconds        | 100 MB            |
| Sample Circuit 2       | 512 bits   | 200,000               | 4.2 seconds                       | 600 MB                                | 1.8 seconds        | 350 MB            | 3.2 seconds           | 450 MB                    | 0.6 seconds        | 120 MB            |
| Your Circuit 3         | 384 bits   | 150,000               | 3.8 seconds                       | 550 MB                                | 1.5 seconds        | 320 MB            | 3.0 seconds           | 420 MB                    | 0.6 seconds        | 110 MB            |



**Contributions are Welcome:**

We are open to contributions from the community to improve this framework and make it even more useful. Feel free to open issues, propose enhancements, or submit pull requests.

Thank you for choosing our framework. We hope it simplifies your Circom testing work and contributes to your success in developing secure and efficient circuits.

