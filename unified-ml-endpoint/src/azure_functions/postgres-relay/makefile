make run:
	func start

setappenv:
	@(\
	echo "setting Azure Function App scope vars for ENV_TYPE:$(ENV_TYPE)"; \
	resource_group=`yq eval '.global.resource_group' conf/$(ENV_TYPE)/azml_deployment.yaml`;\
	az functionapp config appsettings set --name $(FUNCTION_APP_NAME) -g $$resource_group --settings ENV_TYPE=$(ENV_TYPE);\
	az functionapp config appsettings set --name $(FUNCTION_APP_NAME) -g $$resource_group --settings AZURE_CLIENT_SECRET=$(AZURE_CLIENT_SECRET);\
	az functionapp config appsettings set --name $(FUNCTION_APP_NAME) -g $$resource_group --settings AZURE_CLIENT_SECRET_SECONDARY=$(AZURE_CLIENT_SECRET_SECONDARY);\
	)

make deploy:
	func azure functionapp publish $(FUNCTION_APP_NAME)
