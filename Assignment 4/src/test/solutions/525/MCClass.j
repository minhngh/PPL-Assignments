.source MCClass.java
.class public MCClass
.super java.lang.Object
.field static arr [I
.field static i I

.method public static main([Ljava/lang/String;)V
.var 0 is args [Ljava/lang/String; from Label0 to Label1
Label0:
.var 1 is k F from Label0 to Label1
	ldc 5.0
	fstore_1
.var 2 is m F from Label0 to Label1
	ldc 2.0
	fstore_2
	fload_1
	fload_2
	fdiv
	invokestatic io/string_of_float(F)Ljava/lang/String;
	invokestatic io/print(Ljava/lang/String;)V
Label1:
	return
.limit stack 2
.limit locals 3
.end method

.method public <init>()V
.var 0 is this LMCClass; from Label0 to Label1
Label0:
	aload_0
	invokespecial java/lang/Object/<init>()V
Label1:
	return
.limit stack 1
.limit locals 1
.end method

.method public static <clinit>()V
Label0:
	iconst_4
	newarray int
	dup
	iconst_0
	iconst_1
	iastore
	dup
	iconst_1
	iconst_2
	iastore
	dup
	iconst_2
	iconst_3
	iastore
	dup
	iconst_3
	iconst_4
	iastore
	putstatic MCClass/arr [I
	iconst_2
	putstatic MCClass/i I
Label1:
	return
.limit stack 5
.limit locals 0
.end method
