# swagger-parser
At one company I had a lot of API endpoints and Swagger json.
I had a java test framework which used those endpoints.
So I had to have:
- property file
```properties
products.get = /products
estimates.price.get = /estimates/price
estimates.time.get = /estimates/time
me.get = /me
history.get = /history
```
- java parser for this property file
```java
/**
 * Product Types
*/
public static String productsGet = cfgProvider.getProperty("products.get", String.class);
```
So I created a small script to parse the swagger API and produce java file content and property file content

I know that it's just a converter between json and property. But as I found that people sometimes prefer to write
such a kind of files by hand.

## development
Seriously? Ok, so write code/test and push MR. 