"""
SOAP API client usage example.

This example demonstrates how to use SoapClient for testing SOAP web services,
including operation invocation and response handling.
"""

import asyncio

from py_web_automation import Config, SoapClient


async def main():
    """Main function demonstrating SOAP client usage."""

    config = Config(timeout=30, log_level="INFO")
    soap_url = "https://www.w3schools.com/xml/tempconvert.asmx"
    wsdl_url = "https://www.w3schools.com/xml/tempconvert.asmx?WSDL"

    try:
        print("=== SOAP Client Examples ===\n")

        async with SoapClient(soap_url, config, wsdl_url=wsdl_url, soap_version="1.1") as soap:
            # Example 1: Simple SOAP Call
            print("1. Executing simple SOAP operation...")
            result = await soap.call(
                operation="CelsiusToFahrenheit",
                body={"Celsius": "25"},
            )
            print(f"   Status: {result.status_code}")
            print(f"   Success: {result.success}")
            if result.body:
                print(f"   Response body: {result.body[:200]}...")

            # Example 2: SOAP Call with Custom Headers
            print("\n2. Executing SOAP operation with custom headers...")
            result = await soap.call(
                operation="FahrenheitToCelsius",
                body={"Fahrenheit": "77"},
                headers={"X-Custom-Header": "value"},
            )
            print(f"   Status: {result.status_code}")
            print(f"   Success: {result.success}")

            # Example 3: SOAP Call with Authentication
            print("\n3. Executing authenticated SOAP operation...")
            soap.set_auth_token("your-soap-token", token_type="Bearer")
            result = await soap.call(
                operation="CelsiusToFahrenheit",
                body={"Celsius": "30"},
            )
            print(f"   Status: {result.status_code}")
            print(f"   Success: {result.success}")
            soap.clear_auth_token()

            # Example 4: SOAP 1.2 Call
            print("\n4. Executing SOAP 1.2 operation...")
            soap_12 = SoapClient(soap_url, config, soap_version="1.2")
            result = await soap_12.call(
                operation="CelsiusToFahrenheit",
                body={"Celsius": "20"},
            )
            print(f"   Status: {result.status_code}")
            print(f"   Success: {result.success}")
            await soap_12.close()

            # Example 5: Handling SOAP Faults
            print("\n5. Handling SOAP faults...")
            try:
                result = await soap.call(
                    operation="InvalidOperation",
                    body={"invalid": "data"},
                )
                if not result.success:
                    print(f"   SOAP fault detected: {result.error_message}")
            except Exception as e:
                print(f"   Exception caught: {e}")

        print("\n=== SOAP Examples Completed ===")

    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    asyncio.run(main())
