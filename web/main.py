"""
Pygbag Entry Point for Aggravation Web Version
This is the main entry point for the WebAssembly build.
"""
import asyncio
import aggravation_web

async def main():
    """Main async entry point for Pygbag."""
    await aggravation_web.run()

# Run the async main function
asyncio.run(main())
