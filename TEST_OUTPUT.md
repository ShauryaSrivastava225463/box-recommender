
 Full Output:

Found 22 test(s).
Creating test database for alias 'default' ('file:memorydb_default?mode=memory&cache=shared')...
Operations to perform:
  Synchronize unmigrated apps: messages, rest_framework, staticfiles
  Apply all migrations: admin, auth, contenttypes, sessions, shipping
Synchronizing apps without migrations:
  Creating tables...
    Running deferred SQL...
Running migrations:
  Applying contenttypes.0001_initial... OK
  Applying auth.0001_initial... OK
  Applying admin.0001_initial... OK
  Applying admin.0002_logentry_remove_auto_add... OK
  Applying admin.0003_logentry_add_action_flag_choices... OK
  Applying contenttypes.0002_remove_content_type_name... OK
  Applying auth.0002_alter_permission_name_max_length... OK
  Applying auth.0003_alter_user_email_max_length... OK
  Applying auth.0004_alter_user_username_opts... OK
  Applying auth.0005_alter_user_last_login_null... OK
  Applying auth.0006_require_contenttypes_0002... OK
  Applying auth.0007_alter_validators_add_error_messages... OK
  Applying auth.0008_alter_user_username_max_length... OK
  Applying auth.0009_alter_user_last_name_max_length... OK
  Applying auth.0010_alter_group_name_max_length... OK
  Applying auth.0011_update_proxy_permissions... OK
  Applying auth.0012_alter_user_first_name_max_length... OK
  Applying sessions.0001_initial... OK
  Applying shipping.0001_initial... OK
System check identified no issues (0 silenced).

test_create_box (shipping.tests.BoxAPITest.test_create_box) ... ok
test_create_box_missing_field (shipping.tests.BoxAPITest.test_create_box_missing_field)
Missing 'cost' should return 400. ... ok
test_list_boxes_empty (shipping.tests.BoxAPITest.test_list_boxes_empty) ... ok
test_expensive_fits_but_cheaper_doesnt (shipping.tests.FindBestBoxServiceTest.test_expensive_fits_but_cheaper_doesnt)
Only the expensive box is big enough — must return the expensive one. ... ok
test_product_fits_rotated (shipping.tests.FindBestBoxServiceTest.test_product_fits_rotated)
Product is 5x10x20 cm and box is 6x11x21 cm. ... ok
test_product_fits_when_dimensions_are_equal (shipping.tests.FindBestBoxServiceTest.test_product_fits_when_dimensions_are_equal)
A product that is exactly the same size as the box should fit. ... ok
test_returns_cheapest_box_that_fits (shipping.tests.FindBestBoxServiceTest.test_returns_cheapest_box_that_fits)
Two boxes both fit — should pick the cheaper one. ... ok
test_returns_none_when_no_boxes_exist (shipping.tests.FindBestBoxServiceTest.test_returns_none_when_no_boxes_exist)
No boxes in DB → returns None. ... ok
test_returns_none_when_product_is_too_heavy (shipping.tests.FindBestBoxServiceTest.test_returns_none_when_product_is_too_heavy)
Product fits by size but exceeds max_weight → returns None. ... ok
test_returns_none_when_product_is_too_large (shipping.tests.FindBestBoxServiceTest.test_returns_none_when_product_is_too_large)
Product bigger than every box → returns None. ... ok
test_returns_smallest_volume_on_cost_tie (shipping.tests.FindBestBoxServiceTest.test_returns_smallest_volume_on_cost_tie)
Two boxes have same cost — should return the one with smaller volume. ... ok
test_weight_exactly_at_limit_is_accepted (shipping.tests.FindBestBoxServiceTest.test_weight_exactly_at_limit_is_accepted)
Product weight equal to box max_weight should be accepted. ... ok
test_weight_over_limit_is_rejected (shipping.tests.FindBestBoxServiceTest.test_weight_over_limit_is_rejected)
Product weight one gram over max_weight should be rejected. ... ok
test_create_product (shipping.tests.ProductAPITest.test_create_product) ... ok
test_create_product_missing_field (shipping.tests.ProductAPITest.test_create_product_missing_field)
Missing 'weight' should return 400. ... ok
test_list_products_empty (shipping.tests.ProductAPITest.test_list_products_empty) ... ok
test_list_products_returns_all (shipping.tests.ProductAPITest.test_list_products_returns_all) ... ok
test_recommend_message_when_no_box_found (shipping.tests.RecommendBoxAPITest.test_recommend_message_when_no_box_found) ... ok
test_recommend_returns_400_for_missing_product_id (shipping.tests.RecommendBoxAPITest.test_recommend_returns_400_for_missing_product_id) ... ok
test_recommend_returns_404_for_unknown_product (shipping.tests.RecommendBoxAPITest.test_recommend_returns_404_for_unknown_product) ... ok
test_recommend_returns_best_box (shipping.tests.RecommendBoxAPITest.test_recommend_returns_best_box) ... ok
test_recommend_returns_none_when_no_box_fits (shipping.tests.RecommendBoxAPITest.test_recommend_returns_none_when_no_box_fits) ... ok

