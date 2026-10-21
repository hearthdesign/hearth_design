def handle_stripe_webhook(payload, sig_header):
    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError as e:
        # Invalid payload
        return None, 400
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return None, 400

    # Handle the event
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        handle_checkout_session(session)

    return event, 200