import time
import random
from playwright.sync_api import Page, TimeoutError as PlaywrightTimeoutError


def human_type(
	page: Page,
	selector: str,
	text: str,
	min_delay_seconds: float = 0.06,
	max_delay_seconds: float = 0.18,
	click_first: bool = True,
	clear_before: bool = False,
	wait_timeout_ms: int = 10000,
) -> bool:
	"""Type text into an input in a human-like way (single attempt).

	Returns True if successful. On failure, raises RuntimeError.
	"""
	try:
		page.wait_for_selector(selector, timeout=wait_timeout_ms)
		if click_first:
			page.click(selector)
			time.sleep(random.uniform(0.2, 0.6))

		if clear_before:
			page.fill(selector, "")
			time.sleep(random.uniform(0.1, 0.3))

		for character in text:
			page.type(selector, character)
			time.sleep(random.uniform(min_delay_seconds, max_delay_seconds))

		return True
	except (PlaywrightTimeoutError, Exception) as exc:  # noqa: BLE001
		message = f"human_type failed for selector '{selector}': {exc}"
		print(message)
		raise RuntimeError(message) from exc


def human_click(
	page: Page,
	selector: str,
	delay_before_seconds: float = 0.3,
	delay_after_seconds: float = 0.4,
	wait_timeout_ms: int = 10000,
) -> bool:
	"""Click an element with small human-like delays (single attempt).

	Returns True if successful. On failure, raises RuntimeError.
	"""
	try:
		page.wait_for_selector(selector, timeout=wait_timeout_ms)
		time.sleep(delay_before_seconds)
		page.click(selector)
		time.sleep(delay_after_seconds)
		return True
	except (PlaywrightTimeoutError, Exception) as exc:  # noqa: BLE001
		message = f"human_click failed for selector '{selector}': {exc}"
		print(message)
		raise RuntimeError(message) from exc

	
